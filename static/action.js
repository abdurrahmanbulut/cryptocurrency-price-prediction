const coins = [];

const url = "https://api.binance.com/api/v3/ticker/price";
const resultsDiv = document.getElementById("coin-price");


fetch(url)
.then(response => response.json())
.then(data => {
  const usdtPairs = data.filter(coin => coin.symbol.endsWith("USDT"));
    usdtPairs.forEach(pair => {
      const coinName = pair.symbol.replace("USDT", "");
      const coinPrice = pair.price;
      const coin = { name: coinName, price: coinPrice };
      coins.push(coin);
    });
    
    const searchInput = document.getElementById("search");
    const coinInput = document.getElementById("coin");
    
    searchInput.addEventListener("keyup", function() {
      coinInput.value = searchInput.value;
    });
    
    
    const hoursInput = document.getElementById("hours");
    const hourInput = document.getElementById("hour");
    
    hoursInput.addEventListener("keyup", function() {
      hourInput.value = hoursInput.value;
    });
    
    searchInput.addEventListener("input", function() {
    const searchString = searchInput.value.toLowerCase();
    const filteredCoins = coins.filter(function(coin) {
      return coin.name.toLowerCase().includes(searchString);
    });
    
    const html = filteredCoins.map(function(coin) {
      return "<div style='margin-right: 2rem;'>" + coin.name + ": " + coin.price + "</div>";
    }).join("");
    
    resultsDiv.innerHTML = html;
    });
});





