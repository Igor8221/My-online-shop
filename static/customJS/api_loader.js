/* Слушатель события DOMContentLoaded */
document.addEventListener("DOMContentLoaded", function () {
    const apiUrl = "/api/categories-news/";
    const categoriesList = document.getElementById("categories-list");
    const newsList = document.getElementById("latest-news-list");
    const popularProductsList = document.getElementById("popular-products-list");
    
    /* Асинхронная функция fetchCategoriesAndNews */
    async function fetchCategoriesAndNews() {
        /* Попытка загрузки данных */
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error("Ошибка при загрузке данных");
            }
            const data = await response.json();
           
            /*  Очистка контейнеров */
            if (categoriesList) categoriesList.innerHTML = "";
            if (newsList) newsList.innerHTML = "";
            if (popularProductsList) popularProductsList.innerHTML = "";
           
            /* Заполнение списка категорий */
            if (data.categories && data.categories.length > 0 && categoriesList) {
                data.categories.forEach((category) => {
                    const card = document.createElement("div");
                    card.classList.add("category-card");

                    if (category.image) {
                        const img = document.createElement("img");
                        img.src = category.image;
                        img.classList.add("card-img-top");
                        card.appendChild(img);
                    }

                    const cardBody = document.createElement("div");
                    cardBody.classList.add("card-body");

                    const cardTitle = document.createElement("h5");
                    cardTitle.classList.add("card-title", "category-title");
                    cardTitle.innerHTML = `<a href="/category/${category.slug}" class="category-link">${category.name}</a>`;
                    cardBody.appendChild(cardTitle);
                    card.appendChild(cardBody);
                    categoriesList.appendChild(card);
                });
            } else if (categoriesList) {
                categoriesList.innerHTML = "<p>Категории отсутствуют.</p>";
            }
           
            /*  Заполнение списка новостей */
            if (data.latest_news && data.latest_news.length > 0 && newsList) {
                data.latest_news.forEach((news) => {
                    const card = document.createElement("div");
                    card.classList.add("news-card");

                    if (news.image) {
                        const img = document.createElement("img");
                        img.src = news.image;
                        img.classList.add("card-img-top");
                        card.appendChild(img);
                    }

                    const cardBody = document.createElement("div");
                    cardBody.classList.add("card-body");

                    const cardTitle = document.createElement("h5");
                    cardTitle.classList.add("card-title", "news-title");
                    cardTitle.innerHTML = `<a href="/news/${news.id}" class="news-link">${news.title}</a>`;

                    const link = document.createElement("a");
                    link.href = `/news/${news.id}`;
                    link.classList.add("btn", "btn-info");
                    link.innerHTML = "Читать далее";

                    cardBody.appendChild(cardTitle);
                    cardBody.appendChild(link);
                    card.appendChild(cardBody);
                    newsList.appendChild(card);
                });
            } else if (newsList) {
                newsList.innerHTML = "<p>Новостей пока нет.</p>";
            }
            
            /* Заполнение списка популярных товаров */
            if (data.popular_products && data.popular_products.length > 0 && popularProductsList) {
                data.popular_products.forEach((product) => {
                    const card = document.createElement("div");
                    card.classList.add("col-md-4");

                    const productCard = document.createElement("div");
                    productCard.classList.add("card");

                    if (product.images && product.images.length > 0) {
                        const img = document.createElement("img");
                        img.src = product.images[0].image;
                        img.classList.add("card-img-top");
                        productCard.appendChild(img);
                    }

                    const cardBody = document.createElement("div");
                    cardBody.classList.add("card-body");

                    const cardTitle = document.createElement("h5");
                    cardTitle.classList.add("card-title");
                    cardTitle.innerHTML = product.name;

                    const productLink = document.createElement("a");
                    productLink.href = `/products/${product.id}`;
                    productLink.classList.add("btn", "btn-primary");
                    productLink.innerHTML = "Подробнее";

                    cardBody.appendChild(cardTitle);
                    cardBody.appendChild(productLink);
                    productCard.appendChild(cardBody);

                    card.appendChild(productCard);
                    popularProductsList.appendChild(card);
                });
            } else if (popularProductsList) {
                popularProductsList.innerHTML = "<p>Популярных товаров пока нет.</p>";
            }
           
            /* Проверка наличия элементов в корзине */
            if (data.cart_has_items) {
                const cartIcon = document.querySelector('.bi-cart-fill');
                if (cartIcon) {
                    const badge = document.createElement('span');
                    badge.classList.add('badge', 'bg-danger');
                    badge.innerText = '!';
                    cartIcon.parentNode.appendChild(badge);
                }
            }
        
            /*  Обработка ошибок */
        } catch (error) {
            console.error(error);
            if (categoriesList) categoriesList.innerHTML = "<p>Ошибка загрузки категорий.</p>";
            if (newsList) newsList.innerHTML = "<p>Ошибка загрузки новостей.</p>";
            if (popularProductsList) popularProductsList.innerHTML = "<p>Ошибка загрузки популярных товаров.</p>";
        }
    }

    fetchCategoriesAndNews();
});