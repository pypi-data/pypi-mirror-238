import stripe

from .base import BaseService


class StripeService(BaseService):
    def __init__(
        self,
        stripe_key: str
    ) -> None:
        self.stripe_client = stripe
        self.stripe_key = stripe_key
        stripe.api_key = stripe_key
        super().__init__(log_name='stripe.service')

    def create_billing_session(self, customer_id: str, billing_portal_config_id: str):
        try:
            return self.stripe_client.billing_portal.Session.create(
                customer=customer_id,
                configuration=billing_portal_config_id
            )
        except Exception as e:
            print(e)
            return {'error': {'message': str(e)}}

    def create_billing_portal_configuration(self, base_url: str, features, integration_label: str, integration_id: str):
        return self.stripe_client.billing_portal.Configuration.create(
            features=features,
            business_profile={
                "headline": f"Manage your {integration_label} subscription",
                "privacy_policy_url": "https://www.growth-operations.com/privacy-policy",
                "terms_of_service_url": "https://www.growth-operations.com/terms-of-service",
            },
            default_return_url=f"{base_url}/#my-integrations",
            metadata={
                "integration_id": integration_id
            }
        )

    def get_price(self, price_id: str):
        return self.stripe_client.Price.retrieve(price_id, expand=['tiers'])

    def get_product(self, product_id: str):
        return self.stripe_client.Product.retrieve(product_id)

    def cancel_subscription(self, subscription_id: str):
        self.update_subscription(
            subscription_id=subscription_id,
            cancel_at_period_end=True
        )

    def update_subscription(self, subscription_id: str, **kwargs):
        self.stripe_client.Subscription.modify(
            subscription_id,
            **kwargs
        )

    def create_usage_record(self, subscription_item_id: str, quantity):
        return self.stripe_client.SubscriptionItem.create_usage_record(
            subscription_item_id,
            quantity=quantity,
            action='set'
        )
