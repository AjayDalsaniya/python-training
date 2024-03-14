let searchForm = document.querySelector('.search-form')

document.querySelector('#search-btn').onclick = () =>{
    searchForm.classList.toggle('active')
}

window.onscroll = () =>{
    searchForm.classList.remove('active')
}

// const search = () =>{
//     const searchBox = document.getElementById("search-box").value.toUpperCase();
//     const searchItems = document.getElementById("myItemContainer")
//     const items = document.querySelectorAll(".box")
//     const itemName = searchItems.getElementsByTagName("h3")

//     for(var i=0; i < itemName.length; i++){
//         let match = items[i].getElementsByTagName('h3')[0];

//         if(match){
//             let textValue = match.textContent || match.innerHTML

//             if(textValue.toUpperCase().indexOf(searchBox) > -1){
//                 items[i].style.display = "";
//             }else{
//                 items[i].style.display = "none";
//             }
//         }
//     }
// }

