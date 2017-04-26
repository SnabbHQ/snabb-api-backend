from snabb.payment.models import Payment
from snabb.users.models import Profile
from snabb.stripe_utils.utils import *
import decimal


def create_payment(delivery, price):

    # Get Customer
    user = delivery.delivery_quote.quote_user
    profile = Profile.objects.get(profile_apiuser=user)

    # Generate Payment only if not is Enterprise
    if not profile.enterprise:
        customer = get_or_create_customer(user)
        card = get_default_source(customer)  # Get Default Card
        print(card.card_info['id'])
        if not card:
            print ('DEFAULT CARD NOT EXISTS')
        else:
            # Generate Django Payment
            payment = Payment()
            payment.payment_user = user
            payment.payment_delivery = delivery
            payment.amount = decimal.Decimal(delivery.price)

            try:
                currency = self.delivery_quote.tasks.all()\
                    [:1][0].task_place.place_address.\
                    address_city.city_region.region_country.\
                    country_currency.currency
            except Exception as error:
                print(error)
                currency = 'eur'

            payment.currency = currency
            payment.description = str(delivery.delivery_id)
            payment.status = 'processing'
            payment.save()

            # Get Delivery price
            data_charge = {
                'customer': customer,
                'card': card.card_info['id'],
                'amount': payment.amount,
                'currency': payment.currency,
                'description': payment.description
            }
            # Generate charge
            if create_charge(data_charge):
                print ('PAYMENT SUCCESSFUL')
                payment.status = 'completed'
            else:
                payment.status = 'failed'
            payment.save()
