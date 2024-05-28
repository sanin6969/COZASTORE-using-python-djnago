paypal.Buttons({
    createOrder: function(data, actions) {
    
    return actions.order.create({
    
    purchase_units: [{
    
    amount: {
    
    value: '88.44'
    
    }
    
    }]
    
    });
    
    },
    
    OnApprove: function(data, actions) {
    
    return actions.order.capture().then(function(details) {
    
    
    alert('Transaction completed by '+details.payer.name.given_name + '1');
    
    });
    
    }
    
}).render('#paypal-button-container');