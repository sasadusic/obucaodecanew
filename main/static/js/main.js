// alert('test')
// console.log('test')
const menuBtn = document.querySelector(".fa-bars")
const side = document.querySelector('#side')
const home = document.querySelector('#home')

// Theme Toggle
const toggleBtn = document.querySelector('.theme-toggle')

// Provera da li postoji izabrana tema u lokalnom skladištu pregledača
const savedTheme = localStorage.getItem('theme');

// Ako postoji sačuvana tema, primeni je na stranicu
if (savedTheme) {
    document.body.className = savedTheme
}

toggleBtn.onclick = () => {

    // Provera trenutne teme
    const currentTheme = document.body.classList.contains('dark-theme') ? 'light-theme' : 'dark-theme';

    
    // Čuvanje izabrane teme u lokalnom skladištu
    localStorage.setItem('theme', currentTheme);

    const savedTheme = localStorage.getItem('theme');
    document.body.className = savedTheme
};

menuBtn.onclick = () => {
    menuBtn.classList.toggle('fa-times')
    side.classList.toggle('active')
}

const arrowleft = document.querySelector('#arrow-left')
const arrowRight = document.querySelector('#arrow-right')
const detailImages = document.querySelectorAll('.img-detail')
const detailimageNum = detailImages.length

let curImage = 1

if(arrowleft){
    arrowleft.onclick = () => {
        document.querySelector(`.img-detail-${curImage}`).style.display = 'none'
        curImage--
        curImage = curImage < 1 ? detailimageNum : curImage
        document.querySelector(`.img-detail-${curImage}`).style.display = 'block'
    }
}
if(arrowRight){
    arrowRight.onclick = () => {
        document.querySelector(`.img-detail-${curImage}`).style.display = 'none'
        curImage++
        curImage = curImage > detailimageNum ? 1 : curImage
        document.querySelector(`.img-detail-${curImage}`).style.display = 'block'
    }
}

// Modal
const imageModal = document.querySelector('[data-modal-image]')
const imageModalOpen = document.querySelectorAll('.image-modal-open')
const closeImageModal = document.querySelector('.modal-close')

imageModalOpen.forEach(open => {

    open.onclick = () => {
        // console.log('open')
        if(window.innerWidth > 768){
            imageModal.showModal()
        }
    }
})
if(closeImageModal){

    closeImageModal.onclick = () =>  imageModal.close()
}
if(imageModal){

    imageModal.onclick = (e) => {
        // alert('test')
        const dialogDimensions = imageModal.getBoundingClientRect()
        if(
            e.clientX < dialogDimensions.left ||
            e.clientX > dialogDimensions.right ||
            e.clientY < dialogDimensions.top ||
            e.clientY > dialogDimensions.bottom
            ) { imageModal.close()}
        }
    }

const modalLeft = document.querySelector('#previous')
const modalRight = document.querySelector('#next')
const modalImages = document.querySelectorAll('.modal-item')
const modalimageNum = modalImages.length

let curModalImage = 1

if(modalLeft){
modalLeft.onclick = () => {
    // alert('left')
    // console.log('left')
    document.querySelector(`.modal-item-${curModalImage}`).style.display = 'none'
    curModalImage--
    curModalImage = curModalImage < 1 ? modalimageNum : curModalImage
    document.querySelector(`.modal-item-${curModalImage}`).style.display = 'block'
}
}
 if(modalRight){

     modalRight.onclick = () => {
         // alert('left')
         // console.log('left')
         document.querySelector(`.modal-item-${curModalImage}`).style.display = 'none'
         curModalImage++
         curModalImage = curModalImage > modalimageNum ? 1 : curModalImage
         document.querySelector(`.modal-item-${curModalImage}`).style.display = 'block'
        }
    }

// // Search opcija u sva obuca
// document.getElementById('search-input').addEventListener('input', function() {
//     // Čim se unese novo slovo, automatski podnosimo formu
//     document.getElementById('search-form').submit();
// });

// const search = document.getElementById("search-input")
// const searchForm = document.getElementById('search-form')

// search.onkeyup = ()=> searchForm.submit()

// window.onscroll = () => {
//     if (isSearching) return;
//     const topOfPage = window.pageYOffset || document.documentElement.scrollTop;
//     const height = document.documentElement.offsetHeight;
//     const visible = Math.max(0, height - 205 + topOfPage);
//     let countVisible = 0
//     Array.from(document.getElementsByClassName('product')).forEach((prod) => {
//         const prodHeight = prod.clientHeight ;
//         const prodTop = prod.offsetTop;
//         if (prodTop < visible && prodTop + prodHeight > visible) {
//             countVisible++;
//             prod.classList.add('visible');
//         } else {
//             prod.classList.remove('visible');
//         }
//     })
//     document.getElementById('count-of-products').innerHTML = `Prikazano: ${countVisible}/${document.getElementsByClassName('
//     document.getElementById('count-of-products').innerHTML = `Prikazano: ${countVisible}/${Array.from(document
//     document.getElementById('count-of-products').innerHTML = `Ukupno proizvoda: ${document.getElementsByClassName('product
//     document.getElementById('count-of-visibles').innerText = `Prikazano: ${countVisible}/${productsCount}`
// };}