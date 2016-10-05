from flask import Flask, render_template, request
import braintree

app = Flask(__name__)

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="ssvnn9szxgsfvmv5",
                                  public_key="gxy6q24z8ymmz8j9",
                                  private_key="91e2de6b8ecd4a68c8c5aa473ce64425")


@app.route('/')
def hello_world():
    return render_template('index.html',
                           title='Home')


@app.route("/client_token", methods=["GET"])
def client_token():
    return braintree.ClientToken.generate()


@app.route("/checkout", methods=["POST"])
def create_purchase():
  nonce_from_the_client = request.form["payment_method_nonce"]

  result = braintree.Transaction.sale({
      "amount": "10.00",
      "payment_method_nonce": nonce_from_the_client,
      "options": {
          "submit_for_settlement": True
      }
  })
  testing_gateway = braintree.TestingGateway(braintree.Configuration.gateway())
  testing_gateway.settlement_confirm_transaction(result.transaction.id)

  updated_transaction = braintree.Transaction.find(result.transaction.id)
  assert updated_transaction.status == braintree.Transaction.Status.SettlementConfirmed

  return render_template('success.html')

if __name__ == '__main__':
    app.run()
