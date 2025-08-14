
const consumptionForm = document.getElementById("consumption-form");
if (consumptionForm) {
    consumptionForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const select = document.getElementById("food-dropdown");
        // get the selected id
        const foodId = select.value;
        // get the selected name of the food, since its the text of the option
        const foodName = select.options[select.selectedIndex].text;
        // get the food qty value (in the same form) 
        const quantity = document.getElementById("food-qty").value;

        if (!foodId) {
            alert("Please select a food");
            return;
        }
        try {
            // connection to flask (app.py)
            const response = await fetch('/api/add', {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({id: foodId, food: foodName, qty: quantity})
            });

            const data = await response.json();

            // add the info to the list
            // find the list
            const list = document.getElementById("items-list")
            // create a new item on the list 
            const li = document.createElement("li");
            // define the values on the list item (for future fetching)
            li.textContent = `${foodName} — ${quantity} grams`;
            li.classList.add("selected-list");
            li.dataset.food = foodName;          
            li.dataset.id = foodId;          
            li.dataset.qty = quantity;

            list.appendChild(li);

        } catch (error) {
            console.log("Error", error);
        }
    });
}

// function to get the total emissions value and it's new html
const estimateBtn = document.getElementById("estimate-btn");
if (estimateBtn) {
    estimateBtn.addEventListener("click", async (e) => {
        e.preventDefault();

        // get all the list elements form the index (so the foods selected) and make an array 
        const foods = []

        // finds all <li> elements inside the element items-list.
        document.querySelectorAll("#items-list li").forEach(li => {
            foods.push({
                id: li.dataset.id,
                food: li.dataset.food,
                qty: li.dataset.qty
            });
        });

        if (foods.length === 0) {
            alert("Please add at least one food item.");
            return;
        }

        // put array into the hidden input in the estimate form
        document.getElementById('estimate-input').value = JSON.stringify(foods);

        // submit to Flask
        document.getElementById('estimate-form').submit();

    });
}

// listenber to the icon
// const iconBtn = document.getElementById("icon-btn");
// for the info display alert