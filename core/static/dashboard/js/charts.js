document.addEventListener("DOMContentLoaded", function () {
    const revenueCtx = document.getElementById("ordersChart");
    new Chart(revenueCtx, {
        type: "line",
        data: {
            labels: ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            datasets: [{
                label: "Orders / Week",
                data: [10,2,5,6,8,12,4]
            }]
        }
    });
});
