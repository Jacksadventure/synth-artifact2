// Storage Controller

// Item Controller
const ItemCtrl = (function (params) {
  // Item Constructor
  const Item = function (id, name, calories) {
    this.id = id;
    this.name = name;
    this.calories = calories;
  };

  // Data Structure / State
  const data = {
    items: [
      { id: 0, name: "Steak Diner", calories: 1200 },
      { id: 1, name: "Cookie", calories: 400 },
      { id: 2, name: "Eggs", calories: 300 },
    ],
    currentItem: null,
    totalCalories: 0,
  };

  // Public methods
  return {
    logData: function () {
      return data;
    },
  };
})();

// UI Controller
const UICtrl = (function (params) {
  // Public methods
  return {};
})();

// App Controller
const App = (function (ItemCtrl, UICtrl) {
  // Public methods
  return {
    init: function () {
      console.log("Initializing app....");
    },
  };
})(ItemCtrl, UICtrl);

// Initialize App
App.init();
