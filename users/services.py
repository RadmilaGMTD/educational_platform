import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_product(paid):
    product = paid.paid_course.name if paid.paid_course else paid.paid_lesson.name
    stripe_product = stripe.Product.create(name=product)
    return stripe_product.id


def create_price(amount, product):
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(float(amount) * 100),
        product_data={"name": product},
    )
    return price


def create_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
