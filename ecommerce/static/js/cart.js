var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.id
        var image = this.dataset.product
        var action = this.dataset.action
        var price = this.dataset.price
        console.log('productId:', productId, 'image:', image, 'action:', action, 'price:', price)

        console.log('USER:', user)
        addCookieItem(productId, image, price, action)

    })
}

function input_change(value, data_id) {


    if (parseInt(value) <= 0) {
        delete cart[data_id]
    } else {
        cart[data_id]["quantity"] = parseInt(value)
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()


}


function addCookieItem(productId, image, price, action) {

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action === 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}





