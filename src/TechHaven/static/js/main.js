// Start Custom functions
const arrowsDraggingHandler = (target, container, width) => {
    target.forEach((arrow) => {
        arrow.addEventListener("click", (e) => {
            const dataArrowName = e.target.getAttribute('data-arrow_name').toLowerCase();
            container.scrollLeft += dataArrowName == 'left' ? -width : width;
        });
    });
};

const mouseDraggingHandler = (container) => {
    let isDragging = false, startX, startScrollLeft;

    const dragStart = (e) => {
        isDragging = true;
        container.classList.add('dragging');
        startScrollLeft = container.scrollLeft;
        startX = e.pageX;
    };

    const dragging = (e) => {
        if (!isDragging) return;
        container.scrollLeft = startScrollLeft - (e.pageX - startX);
    };

    const dragStop = () => {
        isDragging = false;
        container.classList.remove('dragging');
    };

    container.addEventListener("mousemove", dragging);
    container.addEventListener("mousedown", dragStart);
    document.addEventListener("mouseup", dragStop);
};
// End Custom functions

// Start Category
const categoryHandler = () => {

    const parentCategories = Array.from(document.querySelectorAll('.category .parent-categories .parent-category'));
    const mobilePhones = document.getElementById('mobile-phones');
    const computers = document.getElementById('computers');
    const brands = document.getElementById('brands');
    const accessories = document.getElementById('accessories');
    const electronics = document.getElementById('electronics');
    const parentCategoriesNames = [mobilePhones, computers, brands, accessories, electronics]
    
    const parentCategoriesHandler = (parentCategories) => {
        const removeCategoryShow = (elements) => {
            elements.forEach((elem) => {
                if (elem.classList.contains('category-show')) {
                    elem.classList.remove('category-show');
                }
            });
        };
    
        parentCategories.forEach((parentCategory) => {
            parentCategory.addEventListener("click", (e) => {
                let dataName = e.target.getAttribute('data-name');
        
                if (dataName == 'mobile-phones') {
                    removeCategoryShow(parentCategoriesNames)
                    mobilePhones.classList.add('category-show');
                } else if ((dataName == 'computers')) {
                    removeCategoryShow(parentCategoriesNames)
                    computers.classList.add('category-show');
                } else if ((dataName == 'brands')) {
                    removeCategoryShow(parentCategoriesNames)
                    brands.classList.add('category-show');
                } else if ((dataName == 'accessories')) {
                    removeCategoryShow(parentCategoriesNames)
                    accessories.classList.add('category-show');
                } else if ((dataName == 'electronics')) {
                    removeCategoryShow(parentCategoriesNames)
                    electronics.classList.add('category-show');
                }
            });
        });
    };
    
    parentCategoriesHandler(parentCategories);
    
    const removeCategoryButtons = Array.from(document.querySelectorAll('.category .title i'));
    
    const removeCategoryShow = (buttons) => {
        buttons.forEach((btn) => {
            btn.addEventListener("click", (e) => {
                const parentElem = e.target.parentElement.parentElement.parentElement;
                parentElem.classList.remove('category-show');
            })
        });
    };
    
    removeCategoryShow(removeCategoryButtons);
    
    const selectCategoryButton = document.querySelector('.select-category-button');
    selectCategoryButton.onclick = () => { document.querySelector('.category .parent-categories').classList.toggle('select-category-show')};
};

categoryHandler();
// End Category



// Start Nav Icon
const navIconButton = document.querySelector('header nav .nav-icon'),
      nav = document.querySelector('header nav .nav-links'),
      removeNavButton = document.querySelector('header nav .remove-menu');

navIconButton.onclick = () => { nav.classList.toggle('nav-show')};
removeNavButton.onclick = () => { nav.classList.remove('nav-show')};
// End Nav Icon


const imageSlider = () => {
    const next = document.querySelector('.next'),
          prev = document.querySelector('.prev');
    
    next.addEventListener('click', function(){
        const items = document.querySelectorAll('.item')
        document.querySelector('.slide').appendChild(items[0])
    })
    
    prev.addEventListener('click', function(){
        const items = document.querySelectorAll('.item')
        document.querySelector('.slide').prepend(items[items.length - 1]);
    });
    
    setInterval(() => {prev.click()} , 5000);
};

const bestOfferHandler = () => {
    const productsListDragging = document.querySelector('.products-list'),
          arrowsProductsListDragging = Array.from(document.querySelectorAll('.best-offer #arrow')),
          firstCardWidth = productsListDragging.querySelector('.card').offsetWidth;
    
    arrowsDraggingHandler(arrowsProductsListDragging, productsListDragging, firstCardWidth);
    mouseDraggingHandler(productsListDragging);
};

const reviewsHandler = () => {
    const reviewsDragging = document.querySelector('.reviews .container'),
          arrowsReviewsDragging = Array.from(document.querySelectorAll('.reviews #arrow')),
          reviewsFirstCardWidth = reviewsDragging.querySelector('.reviews .container .card').offsetWidth;
    
    arrowsDraggingHandler(arrowsReviewsDragging, reviewsDragging, reviewsFirstCardWidth);
    mouseDraggingHandler(reviewsDragging);
};

if (location.href == "http://127.0.0.1:8000/") {
    imageSlider();
    bestOfferHandler();
    reviewsHandler();
}

// Start Required Fields Handler
// if (location.href == "http://127.0.0.1:5500/register.html") {
//     const requiredFieldsLabels = Array.from(document.querySelectorAll('.register #register-form form div label'));
//     const requiredFieldsLabelHandler = (labels) => {
//         labels.forEach((elem) => {
//             elem.innerHTML = elem.innerText.replace('*', '<span style="color: red;">*</span>')
//         })
//     };
    
//     requiredFieldsLabelHandler(requiredFieldsLabels);
// }
// End Required Fields Handler

// Start Product Primary
// const sliderHandler = () => {
//     const sliderImageContainerHandler = (containers) => {
//         let target;
//         containers.forEach((container) => {
//             if (container.classList.contains('active')) target = container;
//         });

//         return target;

//     };
//     const sliderViewport = document.querySelector('.image-slider__viewport');
//     const sliderImageContainer = sliderImageContainerHandler(Array.from(document.querySelectorAll('.image-slider__container')));
//     const numOfSliderImages = sliderImageContainer.querySelectorAll('img').length;

//     let sliderOffset = 0;
//     const moveSlides = offset => {
//         const imageWidth = sliderImageContainer.querySelector('img').offsetWidth;
//         sliderImageContainer.style.transform = `translateX(-${offset * imageWidth}px)`;
//     };

//     setInterval(() => {
//         sliderOffset = sliderOffset < numOfSliderImages - 1 ? sliderOffset + 1 : 0;
//          moveSlides(sliderOffset)
//     }, 100000);

//     const prevButton = document.querySelector('.product-primary .prev');
//     const nextButton = document.querySelector('.product-primary .next');

//     prevButton.addEventListener("click", () => {
//         sliderOffset = sliderOffset > 1 ? sliderOffset - 1 : numOfSliderImages -1;
//         moveSlides(sliderOffset)
//     });

//     nextButton.addEventListener("click", () => {
//         sliderOffset = sliderOffset < numOfSliderImages - 1 ? sliderOffset + 1 : 0;
//         moveSlides(sliderOffset);
//     });
// };


// if (window.location.href == 'http://127.0.0.1:5500/product-view.html') {
//     const sliderImageContainers = Array.from(document.querySelectorAll('.image-slider__container')),
//     firstContainer = sliderImageContainers[0],
//     colorSwatches = Array.from(document.querySelectorAll('.color-swatches .color-swatche')),
//     firstSwatche = colorSwatches[0];

//     firstContainer.classList.add('active');
//     firstSwatche.classList.add('active');

//     colorSwatches.forEach(colorSwatche => {
//         colorSwatche.addEventListener("click", (e) => {
//             let targetElem = e.target,
//                 targetElemAttr = targetElem.getAttribute('data-color-id');
    
//             colorSwatches.forEach((elem) => {
//                 elem.classList.remove('active');
//             });
    
//             targetElem.classList.add('active');
    
//             sliderImageContainers.forEach((sliderImageContainer) => {
//                 sliderImageContainers.forEach((elem) => {
    
//                     if (elem.getAttribute('data-image-id') == targetElemAttr) {
//                         elem.classList.add('active');
//                     } else {
//                         elem.classList.remove('active');
//                     }
                    
                    
//                 });
                
//             });
            
//             sliderHandler();
//         });
//     });
    
//     sliderHandler();
// }




// End Product Primary


// Start Product Entire Information
// const productEntireInfoLinks = Array.from(document.querySelectorAll('section#product-entire-info .product-entire-info-links .product-entire-info-link')),
//       productEntireInfoDropDowns = Array.from(document.querySelectorAll('section#product-entire-info .dropdown'));

// const productEntireInfoLinksHandler = (productEntireInfoLinks, productEntireInfoDropDowns) => {
//     productEntireInfoLinks.forEach((productEntireInfoLink) => {
//         productEntireInfoLink.addEventListener("click", (e) => {
//             let targetElement = e.target;
//             productEntireInfoLinks.forEach((elem) => {
//                 elem.classList.remove('active');
//             });
//             productEntireInfoDropDowns.forEach((dropDown) => {
//                 dropDown.classList.remove('active');
//                 if (dropDown.getAttribute('data-name') == targetElement.getAttribute('data-name')) {
//                     dropDown.classList.add('active')
//                 } else {
//                     dropDown.classList.remove('active')
//                 }
//             });
//             targetElement.classList.add('active');
//         });
//     });
// };

// productEntireInfoLinksHandler(productEntireInfoLinks, productEntireInfoDropDowns);

// End Product Entire Information

// Start Profile
// const profileBodyLinks = Array.from(document.querySelectorAll('.profile .container #profile-body .profile-body-links li')),
//       profileBodyDropDowns = Array.from(document.querySelectorAll('.profile .container #profile-body .dropdown'));

// productEntireInfoLinksHandler(profileBodyLinks, profileBodyDropDowns);


// const avatarDiv = document.getElementById('id_avatar').parentElement;

// avatarDiv.querySelector('a').style.display = 'none'

// End Profile

{/* <input type="file" name="avatar" accept="image/*" id="id_avatar"> */}

// const searchBar = document.querySelector('.search-bar form input');


// searchBar.addEventListener("keypress", (e) => {
//     if (e.key === 'Enter') {
//         console.log('Yes')
//     }
// });


