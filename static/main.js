// Modern Food Impact Calculator - JavaScript

// Store selected items
let selectedItems = [];

const consumptionForm = document.getElementById("consumption-form");
if (consumptionForm) {
    consumptionForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const select = document.getElementById("food-dropdown");
        const foodId = select.value;
        const foodName = select.options[select.selectedIndex].text;
        const quantity = document.getElementById("food-qty").value;

        if (!foodId) {
            alert("Please select a food");
            return;
        }
        
        if (!quantity || quantity <= 0) {
            alert("Please enter a valid quantity");
            return;
        }

        try {
            const response = await fetch('/api/add', {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({foodId: foodId, foodName: foodName, quantity: quantity})
            });

            const data = await response.json();

            // Add to selected items array
            selectedItems.push({
                id: foodId,
                food: foodName,
                qty: quantity
            });

            // Update the display
            updateItemsList();

            // Clear inputs
            select.value = "";
            document.getElementById("food-qty").value = "";

        } catch (error) {
            console.error("Error adding food:", error);
            alert("Error adding food. Please try again.");
        }
    });
}

// Update items list display
function updateItemsList() {
    const list = document.getElementById("items-list");
    list.innerHTML = '';
    
    selectedItems.forEach((item, index) => {
        const li = document.createElement("li");
        li.className = "selected-item";
        li.innerHTML = `
            <div class="item-info">
                <span class="item-name">${item.food}</span>
                <span class="item-qty">${item.qty}g</span>
            </div>
            <button type="button" class="item-remove" onclick="removeItem(${index})">
                <i class="bi bi-x-lg"></i>
            </button>
        `;
        list.appendChild(li);
    });
}

// Remove item function
function removeItem(index) {
    selectedItems.splice(index, 1);
    updateItemsList();
}

// Clear all items
function clearAll() {
    if (confirm('Clear all items?')) {
        selectedItems = [];
        updateItemsList();
    }
}

// Handle form submission for estimates
const estimateForm = document.getElementById("estimate-form");
if (estimateForm) {
    estimateForm.addEventListener("submit", (e) => {
        e.preventDefault();

        if (selectedItems.length === 0) {
            alert("Please add at least one food item.");
            return;
        }

        // Put array into the hidden input
        document.getElementById('estimate-input').value = JSON.stringify(selectedItems);

        // Submit to Flask
        estimateForm.submit();
    });
}
