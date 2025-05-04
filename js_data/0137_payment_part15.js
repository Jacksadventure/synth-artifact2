req.type("json");
req.send({
  "delivery_needed": "false",
  "merchant_id":data.Mid,
  "merchant_order_id": RandomStringGen(20),
  "amount_cents": "25000",
  "currency": "EGP",
  "items": [],
  "shipping_data":{
    "first_name": "test_user", 
    "phone_number": "+201003978030", 
    "last_name": "test_user",
    "email": "mr@g.com",
    "apartment": "803",
    "floor": "42",
    "street": "sample street",
    "building": "4055",
    "postal_code": "33221",
    "country": "EG",
    "city": "Cairo"
  }
});