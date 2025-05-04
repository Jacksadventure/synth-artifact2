req.type("json");
req.send({
  "amount_cents": "25000",
  "currency": "EGP",
  "card_integration_id": "184",
  "order_id": data.orderId,
  "billing_data": {
      "apartment": "803", 
      "email": "claudette09@exa.com", 
      "floor": "42", 
      "first_name": "Clifford", 
      "street": "Ethan Land", 
      "building": "8028", 
      "phone_number": "+86(8)9135210487", 
      "shipping_method": "PKG", 
      "postal_code": "01898", 
      "city": "Jaskolskiburgh", 
      "country": "CR", 
      "last_name": "Nicolas", 
      "state": "Utah"
  }
});