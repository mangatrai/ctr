import json
import random
from faker import Faker
from datetime import datetime, timedelta
import uuid

fake = Faker()

def generate_random_transaction():
    def random_date(start_date="-1y", end_date="now"):
        return fake.date_time_between(start_date=start_date, end_date=end_date)

    def random_amount(min_amount=0, max_amount=1000):
        return f"{round(random.uniform(min_amount, max_amount), 2)}"

    def random_status():
        statuses = ["Published", "Pending", "Cancelled", "Completed"]
        return random.choice(statuses)

    transaction_id = f"{random.randint(100, 999)}::{int(datetime.now().timestamp()*1000)}::{random.randint(10, 99)}::{random.randint(10000, 99999)}"

    # Base transaction structure
    transaction = {
        "transactionId": transaction_id,
        "transactionType": random.choice(["SALE", "RETURN", "EXCHANGE"]),
        "transactionSubType": random.choice(["REGULAR", "SPECIAL", ""]),
        "transactionStatusDesc": random_status(),
        "transactionStatusCode": str(random.randint(100, 999)),
        "businessUnitCode": "SEPHORADOTCOM",
        "source": "DIGITAL",
        "isMarkedFraud": random.choice(["Y", "N"]),
        "transactionDate": random_date().isoformat(),
        "allocationRuleId": "MLTNDE",
        "paymentRuleId": "SEPHORADOTCOM",
        "sourcingClassification": "FLASH"
    }

    # Transaction Additional Info
    transaction["transactionAdditionalInfo"] = {
        "sourceTransactionNo": str(random.randint(40000000000, 49999999999)),
        "sellerId": "SEPHORADOTCOM",
        "cashierNumber": str(random.randint(100, 999)),
        "businessDate": fake.date(),
        "locationId": f"{random.randint(1000, 9999)}",
        "terminalNo": f"{random.randint(1000, 9999)}",
        "sequenceNo": str(random.randint(10000, 99999)),
        "tillId": str(random.randint(1, 10)),
        "invoiceNo": str(random.randint(100, 999)),
        "transactionOrigin": random.choice(["iphoneAppV2.0", "webstore", "androidApp"]),
        "riskFactor": random.choice(["noKnownRisk", "lowRisk", "mediumRisk", "highRisk"]),
        "isTaxExempt": random.choice(["Y", "N"]),
        "employeeId": str(random.randint(1000, 9999)),
        "invoiceType": random.choice(["INVOICE", "CREDIT_MEMO", "DEBIT_MEMO"]),
        "adjustmentType": random.choice(["TAX", "PRICE", "QUANTITY"]),
        "profileTaxExemptCode": str(random.randint(100, 999)),
        "isGuestTransaction": random.choice(["Y", "N"]),
        "locale": random.choice(["en_US", "fr_CA", "es_US"]),
        "entryType": random.choice(["ONLINE", "STORE", "MOBILE"]),
        "shopperName": fake.name(),
        "eventName": "ORDER_DROP",
        "eventTimestamp": random_date().isoformat(),
        "orderTotal": random_amount(),
        "merchTotal": random_amount(),
        "shipTotal": random_amount(),
        "isRemorseReq": random.choice(["Y", "N"]),
        "skipFulfillmentHold": random.choice(["Y", "N"]),
        "fulfillmentType": random.choice(["PICKUP", "DELIVERY", "SHIPPING"]),
        "isSelfCancelEligible": random.choice(["Y", "N"]),
    }

    # Transaction Totals
    transaction["transactionTotals"] = {
        "paymentStatus": random.choice(["PAID", "PENDING", "FAILED"]),
        "originalTotalAmount": random_amount(),
        "transactionTotal": random_amount(),
        "totalTax": random_amount(0, 100),
        "totalDiscount": random_amount(0, 50),
        "headerCharges": random_amount(0, 20),
        "headerDiscount": random_amount(0, 30),
        "headerTax": random_amount(0, 50),
        "shippingTotal": random_amount(0, 15),
        "currency": "USD",
        "originGST": random_amount(0, 10),
        "originHST": random_amount(0, 10),
        "originPST": random_amount(0, 10),
        "originMerchTotal": random_amount(),
        "originShipTotal": random_amount(0, 15),
        "originTaxTotal": random_amount(0, 50),
    }

    # Client Info
    transaction["clientInfo"] = {
        "clientFirstName": fake.first_name(),
        "clientLastName": fake.last_name(),
        "clientPhoneNo": fake.phone_number(),
        "clientEmailId": fake.email(),
        "clientLoyaltyId": str(random.randint(1000000, 9999999)),
        "customerId": str(uuid.uuid4()),
        "clientLoyaltyTier": random.choice(["BRONZE", "SILVER", "GOLD", "PLATINUM"])
    }

    # Employee Details
    transaction["employeeDetails"] = {
        "saleEmployeeId": str(random.randint(100, 999)),
        "serviceEmployeeId": str(random.randint(100, 999)),
        "tipAmount": random_amount(0, 20),
        "currencyCode": "USD"
    }

    # Generate Lines
    transaction["lines"] = [{
        "lineId": str(i + 1),
        "lineReferenceNo": str(uuid.uuid4()),
        "lineStatusCode": str(random.randint(100, 999)),
        "lineStatusDesc": random.choice(["Active", "Shipped", "Delivered", "Cancelled"]),
        "lineItemGroup": "PROD",
        "quantity": str(random.randint(1, 5)),
        "lineTotal": random_amount(),
        "unitPrice": random_amount(),
        "shippedQuantity": str(random.randint(1, 5)),
        "isReturnable": random.choice(["Y", "N"]),
        "isMarkdown": random.choice(["Y", "N"]),
        "itemId": str(random.randint(1000000, 9999999)),
        "upc": str(random.randint(100000000000, 999999999999)),
        "unitOfMeasure": "EACH",
        "itemDesc": fake.word().upper() + " " + random.choice(["CREAM", "SERUM", "LOTION", "CLEANSER"]),
        "brand": fake.company(),
        "fulfillmentType": random.choice(["SHIPTOHOME", "PICKUP", "DELIVERY"]),
    } for i in range(random.randint(1, 3))]

    # Generate Shipments
    transaction["shipments"] = [{
        "shipmentId": str(random.randint(100000000, 999999999)),
        "carrierServiceCode": random.choice(["Seph17", "Express", "Standard"]),
        "scac": random.choice(["FEDEX", "UPS", "USPS", "FleetOptics"]),
        "status": random.choice(["SHIPPED", "DELIVERED", "IN_TRANSIT"]),
        "sourcingLocationId": f"{random.randint(1000, 9999)}",
        "expectedDeliveryDate": (datetime.now() + timedelta(days=random.randint(1, 7))).isoformat(),
        "shipDate": (datetime.now() + timedelta(days=random.randint(0, 2))).isoformat(),
        "deliveryMethod": random.choice(["SHP", "PICKUP"]),
        "shipmentType": random.choice(["MERGEABLE", "NOT_MERGEABLE"]),
        "hasMergedOrders": random.choice([True, False]),
        "containers": [{
            "containerNo": str(random.randint(1000000, 9999999)),
            "trackingNo": str(uuid.uuid4()).replace("-", "").upper(),
            "trackingUrl": f"https://tracking.carrier.com/{str(uuid.uuid4())}"
        }]
    }]

    return {"transaction": transaction}

def generate_transactions(count=1000):
    transactions = []
    for i in range(count):
        if i % 100 == 0:
            print(f"Generated {i} transactions...")
        transactions.append(generate_random_transaction())
    return transactions

def save_transactions_to_file(transactions, filename="sample/synthetic_transactions.json"):
    with open(filename, 'w') as f:
        json.dump(transactions, f, indent=2)

if __name__ == "__main__":
    print("Generating synthetic transactions...")
    transactions = generate_transactions(1000)
    save_transactions_to_file(transactions)
    print(f"Generated 1000 synthetic transactions and saved to synthetic_transactions.json")