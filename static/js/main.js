{	
	class Details {
		constructor() {
			this.DOM = {};

			const detailsTmpl = `
			<div class="details__bg details__bg--down">
				<button class="details__close"><i class="fas fa-2x fa-times icon--cross tm-fa-close"></i></button>
				<div class="details__description"></div>
			</div>						
			`;

			this.DOM.details = document.createElement('div');
			this.DOM.details.className = 'details';
			this.DOM.details.innerHTML = detailsTmpl;
			const appendTarget = document.getElementById('tm-wrap') || document.body;
			appendTarget.appendChild(this.DOM.details);
			this.init();
		}
		init() {
			this.DOM.bgDown = this.DOM.details.querySelector('.details__bg--down');
			this.DOM.description = this.DOM.details.querySelector('.details__description');
			this.DOM.close = this.DOM.details.querySelector('.details__close');

			this.initEvents();
		}
		initEvents() {
			document.body.addEventListener('click', () => this.close());
			this.DOM.bgDown.addEventListener('click', function(event) {
							event.stopPropagation();
						});
			this.DOM.close.addEventListener('click', () => this.close());
		}
		fill(info) {
			this.DOM.description.innerHTML = info.description;
		}		
		getProductDetailsRect(){
			let p = 0;
			let d = 0;

			try {
				p = this.DOM.productBg.getBoundingClientRect();
				d = this.DOM.bgDown.getBoundingClientRect();	
			}
			catch(e){}

			return {
				productBgRect: p,
				detailsBgRect: d
			};
		}
		open(data) {
			if(this.isAnimating) return false;
			this.isAnimating = true;

			this.DOM.details.style.display = 'block';  

			this.DOM.details.classList.add('details--open');
			if (data && data.productBg) {
				this.DOM.productBg = data.productBg;
				this.DOM.productBg.style.opacity = 0;
			}
			const rect = this.getProductDetailsRect();

			this.DOM.bgDown.style.transform = `translateX(${rect.productBgRect.left-rect.detailsBgRect.left}px) translateY(${rect.productBgRect.top-rect.detailsBgRect.top}px) scaleX(${rect.productBgRect.width/rect.detailsBgRect.width}) scaleY(${rect.productBgRect.height/rect.detailsBgRect.height})`;
            this.DOM.bgDown.style.opacity = 1;

            console.log("Details box should now be open.");

            // animate background
            anime({
                targets: [this.DOM.bgDown],
                duration: (target, index) => index ? 800 : 250,
                easing: (target, index) => index ? 'easeOutElastic' : 'easeOutSine',
                elasticity: 250,
                translateX: 0,
                translateY: 0,
                scaleX: 1,
                scaleY: 1,                              
                complete: () => this.isAnimating = false
            });

            // animate content
            anime({
                targets: [this.DOM.description],
                duration: 250,
                easing: 'easeOutExpo',                
                // translateY: ['100%',0],
                opacity: 1
            });

            // animate close button
            anime({
                targets: this.DOM.close,
                duration: 250,
                easing: 'easeOutSine',
                translateY: ['100%',0],
                opacity: 1
            });

            this.setCarousel();

            window.addEventListener("resize", this.setCarousel);
		}
		close() {
			if(this.isAnimating) return false;
			this.isAnimating = true;

			this.DOM.details.classList.remove('details--open');

			anime({
                targets: this.DOM.close,
                duration: 100,
                easing: 'easeOutSine',
                translateY: '100%',
                opacity: 0
            });

            anime({
                targets: [this.DOM.description],
                duration: 20,
                easing: 'linear',
                opacity: 0
            });

            const rect = this.getProductDetailsRect();
            anime({
                targets: [this.DOM.bgDown],
                duration: 100,
                easing: 'easeOutSine',                
                translateX: (target, index) => {
                    return index ? rect.productImgRect.left-rect.detailsImgRect.left : rect.productBgRect.left-rect.detailsBgRect.left;
                },
                translateY: (target, index) => {
                    return index ? rect.productImgRect.top-rect.detailsImgRect.top : rect.productBgRect.top-rect.detailsBgRect.top;
                },
                scaleX: (target, index) => {
                    return index ? rect.productImgRect.width/rect.detailsImgRect.width : rect.productBgRect.width/rect.detailsBgRect.width;
                },
                scaleY: (target, index) => {
                    return index ? rect.productImgRect.height/rect.detailsImgRect.height : rect.productBgRect.height/rect.detailsBgRect.height;
                },
                complete: () => {
                    this.DOM.bgDown.style.opacity = 0;
                    this.DOM.bgDown.style.transform = 'none';
					if (this.DOM.productBg) {
                    	this.DOM.productBg.style.opacity = 1;
					}
                    this.DOM.details.style.display = 'none';                    
                    this.isAnimating = false;
                }
            });
		}
		// Slick Carousel
        setCarousel() {
          
	        let slider = $('.details .tm-img-slider');

	        if(slider.length) { 

		        if (slider.hasClass('slick-initialized')) {
		            slider.slick('destroy');
		        }

		        if($(window).width() > 767){
		            // Slick carousel
		            slider.slick({
		                dots: true,
		                infinite: true,
		                slidesToShow: 4,
		                slidesToScroll: 3
		            });
		        }
		        else {
		            slider.slick({
			            dots: true,
			            infinite: true,
			            slidesToShow: 2,
			            slidesToScroll: 1
		        	});
		     	}	
	        }          
        }

        fillCountryData(countryData) {
            let content = `<h2>Top 5 Customers in ${countryData.countryName}</h2>`;
        
            let sortedCustomers = countryData.customers.sort((a, b) => b.total_balance - a.total_balance).slice(0, 10);
        
            content += `<table><thead><tr><th>Rank</th><th>Id</th><th>Name</th><th>Personalnumber</th><th>Address</th><th>City</th><th>Total Balance</th></tr></thead><tbody>`;
        
            sortedCustomers.forEach((customer, index) => {
                const customerUrl = customerDetailUrl.replace('/0', '/' + customer.id);
                content += `<tr onclick="window.location.href='${customerUrl}';" style="cursor:pointer;">
                                <td>${index + 1}</td>
                                <td>${customer.id}</td>
                                <td>${customer.name} ${customer.lastname}</td>
                                <td>${customer.personalnumber}</td>
                                <td>${customer.address}</td>
                                <td>${customer.city}</td>
                                <td>$${customer.total_balance}</td>
                            </tr>`;
            });
        
            content += `</tbody></table>`;
            console.log(content)
            this.DOM.description.innerHTML = content;
        }
        
        fillCustomerData(customerData) {
            let content = `<div class="customer-details-container">`;
        
            // Customer info
            content += `<table class="customer-info-table">
                <tr><th colspan="2">${customerData.GivenName} ${customerData.Surname}</th></tr>
                <tr><td>Birthday:</td><td>${customerData.Birthday}</td></tr>
                <tr><td>Personal Number:</td><td>${customerData.PersonalNumber}</td></tr>
                <tr><td>Address:</td><td>${customerData.Streetaddress}</td></tr>
                <tr><td>Zipcode:</td><td>${customerData.Zipcode}</td></tr>
                <tr><td>City:</td><td>${customerData.City}</td></tr>
                <tr><td>Country:</td><td>${customerData.Country}</td></tr>
                <tr><td>Phone Number:</td><td>${customerData.Telephone}</td></tr>
                <tr><td>Email:</td><td>${customerData.EmailAddress}</td></tr>
            </table>`;
        
            // Account information
            if (customerData.Accounts && customerData.Accounts.length > 0) {
                let totalBalance = 0; 
                content += `<table class="accounts-info-table"><tr><th>Type</th><th>Balance</th></tr>`;
                customerData.Accounts.forEach(account => {
                    let balance = parseFloat(account.Balance);
                    totalBalance += balance; 
                    content += `<tr><td>${account.AccountType}</td><td>$${balance.toLocaleString()} SEK</td></tr>`; // Use toLocaleString() for formatting
                });
                content += `<tr class="total-balance"><td>Total Balance:</td><td>$${totalBalance.toLocaleString()} SEK</td></tr></table>`; // Format total balance
            } else {
                content += `<p>No accounts found</p>`;
            }
            content += `</div>`;
        
            // Action buttons
            const customerDetailUrl = baseCustomerDetailUrl.replace('/0', '/' + customerData.Id);
            content += `<div class="details__actions">
                <a href="${customerDetailUrl}" class="details__button">More Details</a>
            </div>`;
        
            // Append constructed content
            this.DOM.description.innerHTML = content;
            this.DOM.details.classList.add('table-details-box');
        }
	}; // class Details

	class Item {
		constructor(el) {
			this.DOM = {};
			this.DOM.el = el;
			this.DOM.product = this.DOM.el.querySelector('.product');
			this.DOM.productBg = this.DOM.product.querySelector('.product__bg');

			this.info = {
				description: this.DOM.product.querySelector('.product__description').innerHTML
			};

			this.initEvents();
		}
		initEvents() {
			this.DOM.product.addEventListener('click', () => this.open());
		}
		open() {
			if (this.DOM.el.classList.contains('map-container')) {
			} else {
				if (this.DOM.productBg) {
					DOM.details.fill(this.info);
					DOM.details.open({
						productBg: this.DOM.productBg
					});
				}
			}
		}		
	}; // class Item
	class CustomerItem {
		constructor(el) {
			this.DOM = { el: el };
			try {
				console.log(this.DOM.el.getAttribute('data-customer'));
				this.customerData = JSON.parse(this.DOM.el.getAttribute('data-customer'));
			} catch (e) {
				console.error('Error parsing JSON:', e);
				this.customerData = {};
			}
			this.i
			this.initEvents();
		}
		initEvents() {
			this.DOM.el.addEventListener('click', () => {
				DOM.details.fillCustomerData(this.customerData);
				DOM.details.open();
			});
			this.DOM.el.addEventListener('click', () => {
				document.querySelectorAll('.table-row').forEach(row => row.classList.remove('active'));
				this.DOM.el.classList.add('active');
			});
		}
	}; //Customer item class

	class AdminItem {
		constructor(el) {
			this.DOM = { el: el};
			this.DOM.product = this.DOM.el.querySelector('.product');
			this.DOM.productBg = this.DOM.product.querySelector('.product__bg');

			this.info = {
				description: this.DOM.product.querySelector('.product__description').innerHTML
			};

			this.initEvents();
		}
		initEvents() {
			this.DOM.product.addEventListener('click', () => this.open());
		}
		open() {
			if (this.DOM.productBg) {
				DOM.details.fill(this.info);
				DOM.details.open({
					productBg: this.DOM.productBg
				});
			}
		}
	}


	const DOM = {};

    DOM.details = new Details();

	DOM.grid = document.querySelector('.grid');
	if (DOM.grid) {
		DOM.content = DOM.grid.parentNode;
		DOM.gridItems = Array.from(DOM.grid.querySelectorAll('.grid__item')).filter(item => item.querySelector('.product'));
		let items = [];
		DOM.gridItems.forEach(item => items.push(new Item(item)));
	}

	DOM.adminItems = document.querySelectorAll('.user-stat-item');
    if (DOM.adminItems.length) {
        let adminItems = [];
        DOM.adminItems.forEach(item => adminItems.push(new AdminItem(item)));
    }

	if (document.querySelector('.table-list')) {
		DOM.customerRows = document.querySelectorAll('.table-row');
		DOM.customerRows.forEach(row => new CustomerItem(row));
	}

	window.DOM = DOM;
	

	function openDetailsWithData(data) {
		console.log("Data received:", data);  
		DOM.details.fillCountryData(data);
        console.log('It should')
		DOM.details.open(data);
	}
};

$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

// Filter functions
let currentSortColumn = 'Surname';
let currentSortOrder = 'asc';

document.addEventListener('DOMContentLoaded', function() {
    initializeSortingAndFiltering();
});

function initializeSortingAndFiltering() {
    const currentPagePath = window.location.pathname;
    let filterFunction;
    let searchInputId;

    if (currentPagePath.includes('/customers/customer_list')) {
        filterFunction = filterCustomers;
        searchInputId = 'listCustomerSearch';
    } else if (currentPagePath.includes('/account_list')) {
        filterFunction = filterAccounts;
        searchInputId = 'listAccountSearch';
    } else if (currentPagePath.includes('/customers/manage_customer')) {
        filterFunction = filterCustomers;
        searchInputId = 'listCustomerSearch'
    }
    if (filterFunction && searchInputId) {
        setupSorting(filterFunction);

        filterFunction();

        const searchInput = document.getElementById(searchInputId);
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                filterFunction(1, currentSortColumn, currentSortOrder);
            });
        }
    }
}

function setupSorting(filterFunction) {
    document.querySelectorAll('.sortable-column').forEach(column => {
        column.addEventListener('click', function() {
            const sortColumn = this.getAttribute('data-sort-column');
            let newSortOrder = this.getAttribute('data-sort-order') === 'asc' ? 'desc' : 'asc';

            currentSortColumn = sortColumn;
            currentSortOrder = newSortOrder;

            this.setAttribute('data-sort-order', newSortOrder);

            console.log(`Sorting by ${currentSortColumn} in ${currentSortOrder} order`);

            updateSortingUI(this, newSortOrder);
            filterFunction(1, currentSortColumn, currentSortOrder);
        });
    });
}

function updateSortingUI(column, newSortOrder) {
    document.querySelectorAll('.sortable-column').forEach(col => {
        col.innerHTML = col.innerHTML.replace(' ↑', '').replace(' ↓', ''); 
    });

    const arrow = newSortOrder === 'asc' ? ' ↑' : ' ↓';
    column.innerHTML += arrow;
}


function filterCustomers(pageNum = 1, sortColumn = 'Surname', sortOrder = 'asc', searchQueryFromURL = '') {
    let searchQuery = searchQueryFromURL || document.getElementById('listCustomerSearch').value;

    fetch(`/api/customer_lists?search=${encodeURIComponent(searchQuery)}&page=${pageNum}&sort_column=${sortColumn}&sort_order=${sortOrder}`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }
        return response.json(); 
    })
    .then(data => {
        const tbody = document.getElementById('customerListBody');
        if (!tbody) {
            console.error('Tbody element not found');
            return;
        }
        tbody.innerHTML = '';

        if (data.customers && data.customers.length) {
            data.customers.forEach(customer => {
                const row = document.createElement('tr');
                row.className = 'table-row';
                row.setAttribute('data-customer', JSON.stringify(customer));
                row.innerHTML = `
                    <td>${customer.Id}</td>
                    <td>${customer.PersonalNumber}</td>
                    <td>${customer.Surname}, ${customer.GivenName}</td>
                    <td>${customer.Streetaddress}</td>
                    <td>${customer.City}</td>
                    <td>${customer.Country}</td>
                `;

                row.addEventListener('click', () => {
                    DOM.details.fillCustomerData(customer);
                    DOM.details.open();
                });

                tbody.appendChild(row);
            });
			updatePaginationControls(data.pagination);
        } else {
            tbody.innerHTML = '<tr><td colspan="6">No customers found.</td></tr>';
        }
    })
    .catch(error => console.error('Error during fetch:', error));
}

function filterAccounts(pageNum = 1, sortColumn = 'Surname', sortOrder = 'asc') {
    let searchQuery = document.getElementById('listAccountSearch').value;

    fetch(`/account_list?ajax=1&search=${encodeURIComponent(searchQuery)}&page=${pageNum}&sort_column=${sortColumn}&sort_order=${sortOrder}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const tbody = document.querySelector('#accountListBody');
        tbody.innerHTML = '';

        data.customers.forEach(customer => {
            const row = document.createElement('tr');
            row.className = 'table-row';
            let accountsHtml = '<td colspan="2"><table class="inner-table">';

            Object.entries(customer.GroupedAccounts).forEach(([accountType, accountInfo]) => {
                accountsHtml += `<tr><td>${accountType} x ${accountInfo.count}</td><td>${accountInfo.total_balance} SEK</td></tr>`;
            });
            accountsHtml += '</table></td>';

            row.innerHTML = `<td>${customer.Surname}, ${customer.GivenName}</td>${accountsHtml}<td>${customer.total_balance} SEK</td>`;
            
			row.addEventListener('click', () => {
				DOM.details.fillCustomerData(customer);
				DOM.details.open();
			});
			
			tbody.appendChild(row);
        });

        updatePaginationControls(data.pagination);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


// pagination handling
function updatePaginationControls(pagination) {
    console.log(pagination)
    const paginationContainer = document.querySelector('.table-row-pagination');
    paginationContainer.innerHTML = '';

    // Previous page link
    if (pagination.has_prev) {
        const prevLink = document.createElement('a');
        prevLink.href = "#";
        prevLink.innerHTML = "&lt;";
        prevLink.addEventListener('click', (e) => {
            e.preventDefault();
            changePage(pagination.prev_num);
        });
        paginationContainer.appendChild(prevLink);
    }
	// calc for page display amount
	const total_pages = pagination.total_pages;
    const current_page = pagination.current_page;
    const rangeStart = Math.max(1, current_page - 1);
    const rangeEnd = Math.min(total_pages, current_page + 1);

	if (rangeStart > 1) {
        appendPageLink(1);
        if (rangeStart > 2) {
            appendDots();
        }
    }

	for (let i = rangeStart; i <= rangeEnd; i++) {
        appendPageLink(i);
    }

	if (rangeEnd < total_pages) {
        if (rangeEnd < total_pages - 1) {
            appendDots();
        }
        appendPageLink(total_pages);
    }

	// next page link
	if (pagination.has_next) {
        const nextLink = document.createElement('a');
        nextLink.href = "#";
        nextLink.innerHTML = "&gt;";
        nextLink.addEventListener('click', (e) => {
            e.preventDefault();
            changePage(pagination.next_num);
        });
        paginationContainer.appendChild(nextLink);
    }

    function appendPageLink(page) {
        const pageLink = document.createElement('a');
        pageLink.href = "#";
        pageLink.innerText = page;
        if (page === current_page) {
            pageLink.classList.add('active');
        } else {
            pageLink.addEventListener('click', (e) => {
                e.preventDefault();
                changePage(page);
            });
        }
        paginationContainer.appendChild(pageLink);
    }

	function appendDots() {
        const dots = document.createElement('span');
		dots.className = "dots"
        dots.innerText = '...';
        paginationContainer.appendChild(dots);
    }
}

function changePage(pageNum) {
    const currentPagePath = window.location.pathname;
    if (currentPagePath.includes('/customers/customer_list')) {
        filterCustomers(pageNum, currentSortColumn, currentSortOrder);
    } else if (currentPagePath.includes('/account_list')) {
        filterAccounts(pageNum, currentSortColumn, currentSortOrder);
    } else if (currentPagePath.includes('/customers/manage_customer')) {
        filterCustomers(pageNum, currentSortColumn, currentSortOrder);
    }
}

// filter end

// sidebar collapse
document.addEventListener("DOMContentLoaded", function() {
    const sidebarWrapper = document.getElementById('sidebar-wrapper');
    const sidebarToggle = document.getElementById('sidebarToggle');

    function toggleSidebar() {
        const isCollapsed = sidebarWrapper.classList.contains('collapsed');
        sidebarWrapper.classList.toggle('collapsed', !isCollapsed);
        localStorage.setItem('sidebarCollapsed', !isCollapsed);
    }

    const sidebarShouldBeCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (sidebarShouldBeCollapsed) {
        sidebarWrapper.classList.add('collapsed');
    } else {
        sidebarWrapper.classList.remove('collapsed');
    }

    sidebarToggle.addEventListener('click', toggleSidebar);
});

//sidebar end


//Graph functionality
function openGraph(customerId) {
    fetch(`/api/graph_transactions/${customerId}`)
        .then(response => response.json())
        .then(data => {
            renderGraph(data);
        });
}

function renderGraph(data) {
    const ctx = document.getElementById('transactionGraph').getContext('2d');

    const datasets = data.map(account => {
        const last20Balances = account.balances.slice(-20);
        return {
            label: `${account.account_type} (ID: ${account.account_id})`,
            data: last20Balances.map((item, index) => ({
                x: index + 1, 
                y: parseFloat(item.cumulative_balance)
            })),
            fill: false,
            borderColor: getRandomColor(),
            tension: 0.1
        };
    });

    // Create chart with transaction numbers on the x-axis
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: datasets
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    min: 1,
                    title: {
                        display: true,
                        text: 'Transaction'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Balance'
                    }
                }
            }
        }
    });
}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}


const navToggle = document.getElementById('navToggle');
if (navToggle) {
    navToggle.addEventListener('click', function() {
        var linksContainer = document.querySelector('.tm-nav-table-container');
        var mainContent = document.querySelector('.tm-main-content');
        if (linksContainer && mainContent) {
            linksContainer.classList.toggle('active');

            if (linksContainer.classList.contains('active')) {
                mainContent.style.marginTop = (linksContainer.offsetHeight + 60) + 'px';
            } else {
                mainContent.style.marginTop = '60px';
            }
        }
    });
}

// Collapse sidebar when window is too small

document.addEventListener('DOMContentLoaded', function() {
    var navigation = document.getElementById('sidebar-wrapper');

    if (window.innerWidth < 768) {
        navigation.classList.add('collapsed');
    }
});

// dropdown search functionality.

function searchInformation(sourceId) {
    var input = document.getElementById(sourceId);
    var filter = input.value.trim();
    var dropdownId = sourceId === 'headerSearch' ? 'searchDropdown' : 'editCustomerResultsDropdown'; // Assuming you have a dropdown for edit customer results
    var dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = ''; 

    if (!filter) {
        dropdown.style.display = 'none';
        return;
    }

    if (sourceId === 'headerSearch') {
        const filterOption = document.createElement('div');
        filterOption.className = 'dropdown-item filter-option';
        filterOption.textContent = `Filter customer list with "${filter}"`;
        filterOption.addEventListener('click', function() {
            window.location.href = `/customers/customer_list?search=${encodeURIComponent(filter)}`;
        });
        dropdown.appendChild(filterOption);

        const separator = document.createElement('div');
        separator.className = 'dropdown-divider';
        dropdown.appendChild(separator);
    }

    // Fetch specific customer matches
    fetch(`/api/customer_lists?search=${encodeURIComponent(filter)}`)
    .then(response => response.json())
    .then(data => {
        if (data.customers && data.customers.length > 0) {
            data.customers.forEach(customer => appendCustomerToDropdown(customer, dropdown, sourceId));
            dropdown.style.display = 'block';
        } else {
            const noResults = document.createElement('div');
            noResults.className = 'dropdown-item';
            noResults.textContent = 'No matching customers found';
            dropdown.appendChild(noResults);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        dropdown.style.display = 'none';
    });
}

function appendCustomerToDropdown(customer, dropdown, section) {
    let customerDiv = document.createElement('div');
    customerDiv.className = 'dropdown-item';
    customerDiv.textContent = `${customer.Id} ${customer.PersonalNumber} ${customer.Surname},${customer.GivenName} ${customer.Streetaddress} ${customer.City}`;
    if (section === 'headerSearch') {
        customerDiv.addEventListener('click', function() {
            window.location.href = `/customers/customer_detail/${customer.Id}`;
        });
    } else if (section === 'editCustomerSearch') {
        customerDiv.addEventListener('click', function() {
            fillCustomerEditForm(customer); 
            clearOnClick(section)
        });
    }
    dropdown.appendChild(customerDiv);
}

// User management section

function fetchUsers(page=1) {
    fetch(`/get_users?page=${page}`)
    .then(response => response.json())
    .then(data => {
        const userList = document.getElementById('userList');
        const paginationControls = document.getElementById('paginationControls');

        userList.innerHTML = data.users.map(user => 
            `<tr>
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.first_name}</td>
                <td>${user.last_name}
                <td>${user.email}</td>
                <td>${user.role}</td>
            </tr>`
        ).join('');

        paginationControls.innerHTML = '';
        if (data.has_prev) {
            const prevButton = document.createElement('button');
            prevButton.textContent = 'Previous';
            prevButton.onclick = () => fetchUsers(data.prev_num);
            paginationControls.appendChild(prevButton);
        }
        if (data.has_next) {
            const nextButton = document.createElement('button');
            nextButton.textContent = 'Next';
            nextButton.onclick = () => fetchUsers(data.next_num);
            paginationControls.appendChild(nextButton);
        }
    });
}



let currentSection = '';

function searchEditUser(section) {
    console.log(section);
    const input = document.getElementById(section);
    const filter = input.value.trim();
    console.log(filter);
    
    let dropdownId = '';
    if (section === 'editUserSearch') {
        dropdownId = 'editUserResultsDropdown';
    } else if (section === 'changePasswordSearch') {
        dropdownId = 'changePasswordResultsDropdown';
    } else if (section === 'deleteUserSearch') {
        dropdownId = 'deleteUserResultsDropdown';
    }
    const dropdown = document.getElementById(dropdownId);
    
    dropdown.innerHTML = '';

    if (!filter) {
        dropdown.style.display = 'none';
        return;
    }

    fetch(`/api/search_users?search=${encodeURIComponent(filter)}`)
    .then(response => response.json())
    .then(users => {
        if (users.length > 0) {
            users.forEach(user => appendUserToDropdown(user, dropdown, section));
        } else {
            const noResults = document.createElement('div');
            noResults.className = 'user-dropdown-item';
            noResults.textContent = 'No matching users found';
            dropdown.appendChild(noResults);
        }
        dropdown.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        dropdown.style.display = 'none';
    });
}

function appendUserToDropdown(user, dropdown, section) {
    let userDiv = document.createElement('div');
    userDiv.className = 'dropdown-item';
    userDiv.textContent = `${user.id} - ${user.username} - ${user.email}`;
    userDiv.addEventListener('click', () => {
        switch (section) {
            case 'editUserSearch':
                fillEditForm(user);
                break;
            case 'changePasswordSearch':
                fillChangePasswordInfo(user);
                break;
            case 'deleteUserSearch':
                fillDeleteInfo(user);
                break;
        }
        clearOnClick(section);
    });
    dropdown.appendChild(userDiv);
}

function fillEditForm(user) {
    document.querySelector("#userEditForm [name='user_id']").value = user.id;
    document.querySelector("#userEditForm [name='username']").value = user.username;
    document.querySelector("#userEditForm [name='email']").value = user.email;
    document.querySelector("#userEditForm [name='first_name']").value = user.first_name;
    document.querySelector("#userEditForm [name='last_name']").value = user.last_name;
    document.querySelector("#userEditForm [name='information_permission']").checked = user.information_permission === true;
    document.querySelector("#userEditForm [name='management_permission']").checked = user.management_permission === true;
    document.querySelector("#userEditForm [name='admin_permission']").checked = user.admin_permission === true;
    
}
function fillDeleteInfo(user) {
    document.getElementById('deleteUserInfoId').textContent = user.id;
    document.getElementById('deleteUserInfoUsername').textContent = user.username;
    document.getElementById('deleteUserInfoEmail').textContent = user.email;
    document.getElementById('deleteUserInfoFirstName').textContent = user.first_name;
    document.getElementById('deleteUserInfoLastName').textContent = user.last_name;
    document.getElementById('deleteUserInfoRole').textContent = user.role;
    document.getElementById('deleteUserSection').classList.remove('collapse');
}


function fillChangePasswordInfo(user) {
    document.querySelector("#changePasswordForm [name='user_id']").value = user.id;
    document.getElementById('userInfoId').textContent = user.id;
    document.getElementById('userInfoUsername').textContent = user.username;
    document.getElementById('userInfoEmail').textContent = user.email;
    document.getElementById('userInfoFirstName').textContent = user.first_name;
    document.getElementById('userInfoLastName').textContent = user.last_name;
    document.getElementById('userInfoRole').textContent = user.role;
    document.getElementById('changePasswordSection').classList.remove('collapse');
}

function fillCustomerEditForm(customer) {
    document.querySelector("#editCustomerForm [name='id']").value = customer.Id;
    document.querySelector("#editCustomerForm [name='givenname']").value = customer.GivenName;
    document.querySelector("#editCustomerForm [name='surname']").value = customer.Surname;
    document.querySelector("#editCustomerForm [name='email']").value = customer.EmailAddress;
    document.querySelector("#editCustomerForm [name='telephone']").value = customer.Telephone;
    document.querySelector("#editCustomerForm [name='address']").value = customer.Streetaddress;
    document.querySelector("#editCustomerForm [name='city']").value = customer.City;
    document.querySelector("#editCustomerForm [name='zipcode']").value = customer.Zipcode;
    document.querySelector("#editCustomerForm [name='country']").value = customer.Country;
    document.querySelector("#editCustomerForm [name='birthday']").value = formatDate(customer.Birthday);
    document.querySelector("#editCustomerForm [name='personalnumber_last4']").value = extractLast4Digits(customer.PersonalNumber);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0]; 
}

function extractLast4Digits(personalNumber) {
    return personalNumber.split('-').pop();
}


function clearOnClick(section) {
    let inputId, dropdownId;
    switch (section) {
        case 'editUserSearch':
            inputId = 'editUserSearch';
            dropdownId = 'editUserResultsDropdown';
            break;
        case 'changePasswordSearch':
            inputId = 'changePasswordSearch';
            dropdownId = 'changePasswordResultsDropdown';
            break;
        case 'deleteUserSearch':
            inputId = 'deleteUserSearch';
            dropdownId = 'deleteUserResultsDropdown';
            break;
        case 'editUserSearch':
            inputId = 'editUserSearch';
            dropdownId = 'editUserResultsDropdown';
            break;
        case 'editCustomerSearch':
            inputId = 'editCustomerSearch';
            dropdownId = 'editCustomerResultsDropdown';
            break;
    }
    if (inputId) {
        document.getElementById(inputId).value = '';
    }
    if (dropdownId) {
        document.getElementById(dropdownId).style.display = 'none';
    }
}

function clearSearchInput(section, search, dropdown) {
    document.getElementById(section);
    if (search) {
        document.getElementById(search).value = '';
    }
    if (dropdown) {
        document.getElementById(dropdown).style.display = 'none';
    }

    switch (section) {
        case 'clearEditUser':
            resetEditUserForm();
            break;
        case 'clearChangePassword':
            resetChangePasswordForm();
            break;
        case 'clearDeleteSection':
            resetDeleteUserSection();
            break;
        case 'clearEditCustomer':
            resetEditCustomerForm();
            break;
        default:
            console.error('Unknown section for clearing:', section);
    }
}

function resetEditUserForm() {
    const form = document.getElementById('userEditForm');
    if (form) {
        form.reset();
    }
}

function resetEditCustomerForm() {
    const form = document.getElementById('editCustomerForm');
    if (form) {
        form.reset();
    }
}

function resetChangePasswordForm() {
    const form = document.getElementById('changePasswordForm')
    document.getElementById('userInfoId').textContent = '';
    document.getElementById('userInfoUsername').textContent = '';
    document.getElementById('userInfoEmail').textContent = '';
    if (form) {
        form.reset();
    }
}
function resetDeleteUserSection() {
    document.getElementById('deleteUserInfoId').textContent = '';
    document.getElementById('deleteUserInfoUsername').textContent = '';
    document.getElementById('deleteUserInfoEmail').textContent = '';
    document.getElementById('deleteUserInfoFirstName').textContent = '';
    document.getElementById('deleteUserInfoLastName').textContent = '';
    document.getElementById('deleteUserInfoRole').textContent = '';
}


document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('search'); 
    if (searchQuery) {
        filterCustomers(1, 'Surname', 'asc', searchQuery);
    }
});

document.getElementById('toggleDarkMode').addEventListener('click', function() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });
  
  document.addEventListener('DOMContentLoaded', (event) => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
  });

window.openDetailsWithData = openDetailsWithData;

