# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio

from headless.ext.fedex import FedexClient


async def main():
    params = {
        'url': 'https://apis-sandbox.fedex.com',
        'client_id': 'l7c4e8b137c8594953b246da00a081c2b8',
        'client_secret': '606ad1a9fdd746c8a8352c19cd51f515'
    }
    async with FedexClient(**params) as client:
        response = await client.post(
            url='/ship/v1/shipments',
            json={
                "accountNumber": {"value": "801014461"},
                "labelResponseOptions": "URL_ONLY",
                'mergeLabelDocOption': 'LABELS_ONLY',
                'requestedShipment': {
                    'shipper': {
                        'contact': {
                            #'personName': "Laili Ishaqzai",
                            'phoneNumber': '+31634002222',
                            'companyName': 'Molano B.V.'
                        },
                        'address': {
                            'streetLines': ['Weerenweg 18'],
                            'city': 'Zwanenburg',
                            'postalCode': '1161AJ',
                            'countryCode': 'NL'
                        }
                    },
                    'recipients': [{
                        'contact': {
                            'personName': 'Cochise Ruhulessin',
                            'phoneNumber': '+31687654321',
                            'companyName': 'Immortal Industries B.V.'
                        },
                        'address': {
                            'streetLines': [
                                'Carl-Metz-Str. 4'
                            ],
                            'city': 'Ettlingen',
                            'postalCode': '76275',
                            'countryCode': 'DE'
                        }
                    }],
                    'customsClearanceDetail': {
                        'totalCustomsValue': {'amount': 0, 'currency': 'EUR'},
                        'dutiesPayment': {'paymentType': 'SENDER'},
                        'commodities': [
                            {
                                'countryOfManufacture': 'CN',
                                'unitPrice': {'amount': 1, 'currency': 'EUR'},
                                'quantity': 1,
                                'quantityUnits': 'EA',
                                'description': 'iPhone 12 Pro Max',
                                'weight': {'units': 'LB', 'value': 1}
                            },
                        ]
                    },
                    "shipDatestamp": "2023-11-02",
                    "serviceType": "FEDEX_INTERNATIONAL_PRIORITY",
                    "packagingType": "YOUR_PACKAGING",
                    "pickupType": "USE_SCHEDULED_PICKUP",
                    "blockInsightVisibility": False,
                    "shippingChargesPayment": {"paymentType": "SENDER"},
                    "labelSpecification": {
                        "imageType": "PNG",
                        "labelStockType": "PAPER_4X6"
                    },
                    "requestedPackageLineItems": [
                        {
                            "weight": {"units": "LB", "value": 4},
                            "packageSpecialServices": {
                                #"specialServiceTypes": ["DANGEROUS_GOODS"],
                                #'dangerousGoodsDetail': {
                                #    'accessibility': "ACCESSIBLE",
                                #    'options': ['BATTERY']
                                #},
                                'batteryDetails': [{
                                    'batteryPackingType': 'CONTAINED_IN_EQUIPMENT',
                                    'batteryMaterialType': 'LITHIUM_ION',
                                }]
                            },
                        }
                    ]
                },
            }
        )
        print(response.content)

if __name__ == '__main__':
    asyncio.run(main())