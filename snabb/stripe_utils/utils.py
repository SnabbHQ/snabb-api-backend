from snabb.payment.models import Payment, Card as CardDjango
from snabb.utils.code_response import get_response
from pinax.stripe.models import Card, Customer
from pinax.stripe.actions import charges, customers, sources


def get_or_create_customer(user):
    '''
        Get or create a customer stripe from a user
    '''
    customer = customers.get_customer_for_user(user=user)
    if customer is None:
        customer = customers.create(user=user)
    return customer


def create_card(customer, token):
    '''
        Creates a new card and erases duplicate cards.
        Returns the selected card
    '''
    # Create New Card
    new_card = sources.create_card(customer=customer, token=token)
    card_selected = new_card

    # Delete Duplicated Cards
    if len(customer.stripe_customer.sources.data) > 0:
        cont = 0
        for card in customer.stripe_customer.sources:
            if new_card.fingerprint == card.fingerprint:
                if cont == 0:
                    card_selected = card
                cont += 1
                if cont > 1:
                    sources.delete_card(customer, card.id)
    return card_selected  # Return Selected Card

def get_default_source(customer):
    '''
        Get default Source to customer.
    '''
    try:
        card = CardDjango.objects.get(
            user_id=customer.user,
            default_card=True
        )
        return card
    except CardDjango.DoesNotExist:
        return None

def set_default_source(customer, card_id):
    '''
        Set default Source to customer.
    '''
    customers.set_default_source(customer, card_id)
    cards = CardDjango.objects.filter(
        user_id=customer.user
    )
    if cards.count() <= 0:
        return get_response(400606)
    for card in cards:
        if card.card_info['id'] == card_id:
            card.default_card = True
        else:
            card.default_card = False
        card.save()
    return get_response(200209)


def delete_all_cards(customer):
    '''
        Erases all cards from Customer
    '''
    for card in customer.stripe_customer.sources:
        sources.delete_card(customer, card.id)


def create_charge(data):
    '''
        Create a charge from customer and card
    '''
    if customers.can_charge:
        try:
            charge = charges.create(
                customer=data['customer'],
                source=data['card'],
                amount=Decimal(data['card']),
                currency=data['currency'],
                description=data['description']
            )
            return True
        except Exception as error:
            return False
    return False


def sync_stripe_data(customer):
    '''
        Sync Data from Django to Stripe
    '''
    customers.sync_customer(customer)
    charges.sync_charges_for_customer(customer)
