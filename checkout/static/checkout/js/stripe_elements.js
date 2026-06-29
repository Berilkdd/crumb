const stripePublicKey = document.getElementById("id_stripe_public_key").textContent.slice(1, -1);
const clientSecret = document.getElementById("id_client_secret").textContent.slice(1, -1);

const stripe = Stripe(stripePublicKey);

const elements = stripe.elements();

const style = {
    base: {
        color: "#661E0F",
        fontFamily: '"Poppins", sans-serif',
        fontSize: "16px",
        iconColor: "#661E0F",
        "::placeholder": {
            color: "#C1A392",
        },
    },
    invalid: {
        color: "#dc3545",
        iconColor: "#dc3545",
    },
};

const card = elements.create("card", { style: style });

card.mount("#card-element");

card.addEventListener("change", function (event) {
    const errorDiv = document.getElementById("card-errors");

    if (event.error) {
        errorDiv.textContent = event.error.message;
    } else {
        errorDiv.textContent = "";
    }
});

const form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
    ev.preventDefault();

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        },
    }).then(function (result) {

        if (result.error) {

            document.getElementById("card-errors").textContent = result.error.message;

        } else if (result.paymentIntent.status === "succeeded") {

            form.submit();

        }

    });
});