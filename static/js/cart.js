
// Search Filtering  Function 
const filter = document.querySelector('.search');
filter.addEventListener('keyup', filterTasks);
function filterTasks(e) {
	const text = e.target.value.toLowerCase();
  
	document.querySelectorAll('.collection-item').forEach(function(task){
	  const item = task.getElementsByClassName('product-namee')[0].textContent;
	  if(item.toLowerCase().indexOf(text) != -1){
		task.style.display = 'block';
	  } else {
		task.style.display = 'none';
	  }
	});
  }


// the process of Fetching data of update items in the orderitems in DataBase
//  1-get all products from index.html or from checkout.html or singl-product.html by update-cart class 
//  2-loop throw every product 
//  3-check eventlisteners for every one  If clicked Add to cart then: 
		//  4-Get The Product Id That Clicked 
		//  5-Get The Action ('add' or 'delete') noice ---->in index.html there is just 'add'  in checkout.html 'add' or 'remove'
		//  6 Check The User  Is Authenticated Or Not 
		//  7-If authenticated call  updateUserOrder() Function If Not Call addToCookie()
		//   updateUserOrder function process :
		//     1- Fetch the api  'http://127.0.0.1:8000/user/UpdateItem/'
		//     2-Send Post Data For The API Function (in views.py )
		//     3-The Data We send Is Product id And action(add or remove)
var updateBtns = document.getElementsByClassName('update-cart')
for (i = 0; i < updateBtns.length; i++) {
	
	updateBtns[i].addEventListener('click', function(){
		console.log('update-cart clicked')
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addToCookie(productId, action);
			
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function addToCookie(productId, action){
	if (action=='add'){
		if (cart[productId]== undefined){
			cart[productId] ={'quantity':1};
		}
		else{
			cart[productId]['quantity'] +=1;
		}

	}

	if(action=='remove'){
		cart[productId]['quantity'] -=1;
		if(cart[productId]['quantity'] <=0){
			console.log('delete item');
			delete cart[productId]
		}
	}

	console.log('cart',cart);
	// update the cart in Cookei
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = 'http://127.0.0.1:8000/user/UpdateItem/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}



