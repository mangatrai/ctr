# OpenSearch Reference Queries

## 1. Complex Order Search with Facets (Based on SOLR Query #1)
Demonstrates multi-field search with faceted results and sorting.
```
GET transaction_history/_search
{
  "query": {
    "bool": {
      "should": [
        { "term": { "transaction.transactionId.keyword": "524::1742938725999::84::48748" }},
        { "term": { "transaction.transactionAdditionalInfo.sourceTransactionNo.keyword": "42026467496" }},
        { "term": { "transaction.associatedTransaction.sourceTransactionNo.keyword": "42026467496" }}
      ],
      "minimum_should_match": 1
    }
  },
  "sort": [
    { "transaction.transactionDate": "desc" }
  ],
  "aggs": {
    "by_status": {
      "terms": {
        "field": "transaction.transactionStatusDesc.keyword",
        "size": 5
      }
    },
    "by_source": {
      "terms": {
        "field": "transaction.source.keyword",
        "size": 5
      }
    }
  }
}
```

## 2. Advanced Client Profile Search (Based on SOLR Queries #2, #3, #4)
Demonstrates full-text search with fuzzy matching, boosting, and complex conditions.
```
GET transaction_history/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "multi_match": {
            "query": "Jacob",
            "fields": [
              "transaction.clientInfo.clientFirstName.keyword^2",
              "transaction.clientInfo.clientLastName.keyword"
            ],
            "type": "best_fields",
            "operator": "and",
            "fuzziness": "AUTO"
          }
        },
        {
          "term": {
            "transaction.clientInfo.clientEmailId.keyword": "belltrevor@example.com"
          }
        }
      ],
      "should": [
        {
          "term": {
            "transaction.clientInfo.clientLoyaltyTier.keyword": "GOLD"
          }
        }
      ],
      "minimum_should_match": 1
    }
  },
  "highlight": {
    "fields": {
      "transaction.clientInfo.clientFirstName.keyword": {},
      "transaction.clientInfo.clientLastName.keyword": {}
    },
    "pre_tags": ["<em>"],
    "post_tags": ["</em>"]
  },
  "aggs": {
    "loyalty_distribution": {
      "terms": {
        "field": "transaction.clientInfo.clientLoyaltyTier.keyword"
      }
    }
  }
}
```

## 3. Advanced Status Analysis (Based on SOLR Query #12)
Demonstrates complex date range queries with multiple aggregations and nested conditions.
```
GET transaction_history/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "terms": {
            "transaction.transactionStatusDesc.keyword": ["Pending", "Cancelled"]
          }
        },
        {
          "range": {
            "transaction.transactionDate": {
              "gte": "2024-04-15T00:00:00",
              "lte": "2024-04-16T00:00:00"
            }
          }
        }
      ],
      "should": [
        {
          "term": {
            "transaction.source.keyword": "DIGITAL"
          }
        }
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "status_counts": {
      "terms": {
        "field": "transaction.transactionStatusDesc.keyword"
      }
    },
    "hourly_distribution": {
      "date_histogram": {
        "field": "transaction.transactionDate",
        "calendar_interval": "hour"
      },
      "aggs": {
        "status_by_hour": {
          "terms": {
            "field": "transaction.transactionStatusDesc.keyword"
          }
        }
      }
    },
    "source_distribution": {
      "terms": {
        "field": "transaction.source.keyword"
      }
    }
  }
}
```

## 4. Complex Payment Analysis (Based on SOLR Query #17, #18)
Demonstrates nested queries with multiple conditions and payment analytics.
```
GET transaction_history/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "nested": {
            "path": "paymentMethods",
            "query": {
              "bool": {
                "must": [
                  { "term": { "paymentMethods.paymentType.keyword": "CREDIT_CARD" }},
                  { "term": { "paymentMethods.tenderType.keyword": "VISA" }}
                ],
                "should": [
                  { "range": { "paymentMethods.amount": { "gte": 100 } }}
                ],
                "minimum_should_match": 1
              }
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "payment_methods": {
      "nested": {
        "path": "paymentMethods",
        "aggs": {
          "by_type": {
            "terms": {
              "field": "paymentMethods.paymentType.keyword"
            },
            "aggs": {
              "by_tender": {
                "terms": {
                  "field": "paymentMethods.tenderType.keyword"
                },
                "aggs": {
                  "total_amount": {
                    "sum": {
                      "field": "paymentMethods.amount"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 5. Advanced Store Transaction Analysis (Based on SOLR Query #43)
Demonstrates complex store transaction analysis with multiple conditions and metrics.
```
GET transaction_history/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.transactionAdditionalInfo.sequenceNo.keyword": "49805" }},
        { "term": { "transaction.transactionAdditionalInfo.locationId.keyword": "9848" }},
        { "term": { "transaction.transactionAdditionalInfo.terminalNo.keyword": "3433" }},
        { "term": { "transaction.transactionAdditionalInfo.businessDate": "1989-09-14" }}
      ],
      "should": [
        { "term": { "transaction.transactionType.keyword": "SALE" }},
        { "term": { "transaction.transactionType.keyword": "RETURN" }}
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "by_transaction_type": {
      "terms": {
        "field": "transaction.transactionType.keyword"
      },
      "aggs": {
        "total_amount": {
          "sum": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "item_count": {
          "sum": {
            "field": "transaction.transactionTotals.itemCount"
          }
        }
      }
    }
  }
}
```

## 6. Advanced Transaction Analytics (Based on SOLR Query #46, #47, #48)
Demonstrates complex transaction analytics with multiple dimensions and metrics.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.transactionType.keyword": "SALE" }},
        { "term": { "transaction.source.keyword": "DIGITAL" }}
      ],
      "should": [
        { "term": { "transaction.transactionStatusDesc.keyword": "COMPLETED" }},
        { "term": { "transaction.transactionStatusDesc.keyword": "PENDING" }}
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "by_type": {
      "terms": {
        "field": "transaction.transactionType.keyword",
        "size": 10,
        "order": {
          "total_amount": "desc"
        }
      },
      "aggs": {
        "total_amount": {
          "sum": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "by_source": {
          "terms": {
            "field": "transaction.source.keyword",
            "size": 5
          },
          "aggs": {
            "source_amount": {
              "sum": {
                "field": "transaction.transactionTotals.totalAmount"
              }
            }
          }
        },
        "daily_trend": {
          "date_histogram": {
            "field": "transaction.transactionDate",
            "calendar_interval": "day"
          },
          "aggs": {
            "daily_amount": {
              "sum": {
                "field": "transaction.transactionTotals.totalAmount"
              }
            }
          }
        }
      }
    }
  }
}
```

## 7. Advanced Risk Analysis (Based on Transaction Risk Factors)
Demonstrates complex risk analysis with multiple dimensions and scoring.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.transactionAdditionalInfo.riskFactor.keyword": "highRisk" }}
      ],
      "should": [
        { "term": { "transaction.source.keyword": "DIGITAL" }},
        { "term": { "transaction.source.keyword": "MOBILE" }}
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "risk_analysis": {
      "composite": {
        "sources": [
          {
            "by_status": {
              "terms": {
                "field": "transaction.transactionStatusDesc.keyword"
              }
            }
          },
          {
            "by_source": {
              "terms": {
                "field": "transaction.source.keyword"
              }
            }
          }
        ],
        "size": 100
      },
      "aggs": {
        "total_amount": {
          "sum": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "avg_amount": {
          "avg": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        }
      }
    },
    "risk_trend": {
      "date_histogram": {
        "field": "transaction.transactionDate",
        "calendar_interval": "day"
      },
      "aggs": {
        "risk_count": {
          "value_count": {
            "field": "transaction.transactionAdditionalInfo.riskFactor.keyword"
          }
        }
      }
    }
  }
}
```

## 8. Advanced Shipping Analysis (Based on SOLR Query #16)
Demonstrates complex shipping analysis with nested aggregations and status tracking.
```
GET transaction_history/_search
{
  "query": {
    "bool": {
      "must": [
        { 
          "term": { 
            "transaction.shipments.status.keyword": "IN_TRANSIT"
          }
        }
      ],
      "should": [
        { "term": { "transaction.shipments.deliveryMethod.keyword": "EXPRESS" }},
        { "term": { "transaction.shipments.deliveryMethod.keyword": "STANDARD" }}
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "by_delivery_method": {
      "terms": {
        "field": "transaction.shipments.deliveryMethod.keyword"
      },
      "aggs": {
        "by_status": {
          "terms": {
            "field": "transaction.shipments.status.keyword"
          }
        },
        "avg_delivery_time": {
          "avg": {
            "field": "transaction.shipments.deliveryTime"
          }
        }
      }
    },
    "shipping_trend": {
      "date_histogram": {
        "field": "transaction.transactionDate",
        "calendar_interval": "day"
      },
      "aggs": {
        "by_status": {
          "terms": {
            "field": "transaction.shipments.status.keyword"
          }
        }
      }
    }
  }
}
```

## 9. Advanced Client Loyalty Analysis (Based on SOLR Query #41, #42)
Demonstrates complex customer loyalty analysis with multiple metrics and trends.
```
GET transaction_history/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.clientInfo.clientLoyaltyTier.keyword": "GOLD" }}
      ],
      "should": [
        { "term": { "transaction.transactionType.keyword": "SALE" }},
        { "term": { "transaction.transactionType.keyword": "RETURN" }}
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "by_loyalty": {
      "terms": {
        "field": "transaction.clientInfo.clientLoyaltyTier.keyword"
      },
      "aggs": {
        "transaction_types": {
          "terms": {
            "field": "transaction.transactionType.keyword"
          },
          "aggs": {
            "total_amount": {
              "sum": {
                "field": "transaction.transactionTotals.totalAmount"
              }
            }
          }
        },
        "monthly_trend": {
          "date_histogram": {
            "field": "transaction.transactionDate",
            "calendar_interval": "month"
          },
          "aggs": {
            "monthly_amount": {
              "sum": {
                "field": "transaction.transactionTotals.totalAmount"
              }
            }
          }
        }
      }
    }
  }
}
```

## 10. Advanced Transaction Origin Analysis (Based on SOLR Query #47)
Demonstrates complex source analysis with time-based aggregations and multiple metrics.
```
GET transaction_history/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.transactionAdditionalInfo.transactionOrigin.keyword": "webstore" }}
      ],
      "should": [
        { "term": { "transaction.transactionStatusDesc.keyword": "COMPLETED" }},
        { "term": { "transaction.transactionStatusDesc.keyword": "PENDING" }}
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "daily_transactions": {
      "date_histogram": {
        "field": "transaction.transactionDate",
        "calendar_interval": "day"
      },
      "aggs": {
        "by_status": {
          "terms": {
            "field": "transaction.transactionStatusDesc.keyword"
          },
          "aggs": {
            "total_amount": {
              "sum": {
                "field": "transaction.transactionTotals.totalAmount"
              }
            },
            "avg_amount": {
              "avg": {
                "field": "transaction.transactionTotals.totalAmount"
              }
            }
          }
        },
        "by_payment": {
          "nested": {
            "path": "paymentMethods",
            "aggs": {
              "payment_types": {
                "terms": {
                  "field": "paymentMethods.paymentType.keyword"
                }
              }
            }
          }
        }
      }
    },
    "source_metrics": {
      "terms": {
        "field": "transaction.source.keyword"
      },
      "aggs": {
        "total_amount": {
          "sum": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "transaction_count": {
          "value_count": {
            "field": "transaction.transactionId.keyword"
          }
        }
      }
    }
  }
}
```

## 11. Advanced Price Analysis (Based on SOLR Query #19)
Demonstrates complex price analysis with range queries and multiple aggregations.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "transaction.transactionTotals.totalAmount": {
              "gte": 100,
              "lte": 1000
            }
          }
        }
      ],
      "should": [
        { "term": { "transaction.transactionType.keyword": "SALE" }},
        { "term": { "transaction.transactionType.keyword": "RETURN" }}
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "price_ranges": {
      "range": {
        "field": "transaction.transactionTotals.totalAmount",
        "ranges": [
          { "to": 100 },
          { "from": 100, "to": 500 },
          { "from": 500, "to": 1000 },
          { "from": 1000 }
        ]
      },
      "aggs": {
        "by_status": {
          "terms": {
            "field": "transaction.transactionStatusDesc.keyword"
          }
        }
      }
    },
    "price_stats": {
      "stats": {
        "field": "transaction.transactionTotals.totalAmount"
      }
    }
  }
}
```

## 12. Advanced Item Analysis (Based on SOLR Query #20)
Demonstrates nested item analysis with multiple conditions and metrics.
```
GET transaction_history/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "nested": {
            "path": "transactionDetails",
            "query": {
              "bool": {
                "must": [
                  { "term": { "transactionDetails.itemType.keyword": "PRODUCT" }},
                  { "range": { "transactionDetails.quantity": { "gte": 2 } }}
                ]
              }
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "items": {
      "nested": {
        "path": "transactionDetails",
        "aggs": {
          "by_category": {
            "terms": {
              "field": "transactionDetails.itemCategory.keyword"
            },
            "aggs": {
              "total_quantity": {
                "sum": {
                  "field": "transactionDetails.quantity"
                }
              },
              "total_amount": {
                "sum": {
                  "field": "transactionDetails.lineTotal"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 13. Advanced Employee Analysis (Based on SOLR Query #21)
Demonstrates employee performance analysis with multiple metrics.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.employeeDetails.employeeType.keyword": "STORE" }}
      ]
    }
  },
  "aggs": {
    "by_employee": {
      "terms": {
        "field": "transaction.employeeDetails.employeeId.keyword",
        "size": 10,
        "order": {
          "total_sales": "desc"
        }
      },
      "aggs": {
        "total_sales": {
          "sum": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "transaction_count": {
          "value_count": {
            "field": "transaction.transactionId.keyword"
          }
        },
        "by_status": {
          "terms": {
            "field": "transaction.transactionStatusDesc.keyword"
          }
        }
      }
    }
  }
}
```

## 14. Advanced Location Analysis (Based on SOLR Query #22)
Demonstrates location-based analysis with geographic aggregations.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.transactionAdditionalInfo.locationType.keyword": "STORE" }}
      ]
    }
  },
  "aggs": {
    "by_location": {
      "terms": {
        "field": "transaction.transactionAdditionalInfo.locationId.keyword",
        "size": 10
      },
      "aggs": {
        "total_sales": {
          "sum": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "by_region": {
          "terms": {
            "field": "transaction.transactionAdditionalInfo.region.keyword"
          }
        },
        "daily_trend": {
          "date_histogram": {
            "field": "transaction.transactionDate",
            "calendar_interval": "day"
          }
        }
      }
    }
  }
}
```

## 15. Advanced Discount Analysis (Based on SOLR Query #23)
Demonstrates complex discount analysis with nested aggregations.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {
          "nested": {
            "path": "priceModifiers",
            "query": {
              "bool": {
                "must": [
                  { "term": { "priceModifiers.modifierType.keyword": "DISCOUNT" }},
                  { "range": { "priceModifiers.amount": { "gt": 0 } }}
                ]
              }
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "discounts": {
      "nested": {
        "path": "priceModifiers",
        "aggs": {
          "by_type": {
            "terms": {
              "field": "priceModifiers.modifierType.keyword"
            },
            "aggs": {
              "total_discount": {
                "sum": {
                  "field": "priceModifiers.amount"
                }
              },
              "avg_discount": {
                "avg": {
                  "field": "priceModifiers.amount"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 16. Advanced Customer Segmentation (Based on SOLR Query #24)
Demonstrates customer segmentation with multiple criteria.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.clientInfo.clientType.keyword": "REGULAR" }}
      ]
    }
  },
  "aggs": {
    "customer_segments": {
      "composite": {
        "sources": [
          {
            "loyalty_tier": {
              "terms": {
                "field": "transaction.clientInfo.clientLoyaltyTier.keyword"
              }
            }
          },
          {
            "total_spent": {
              "range": {
                "field": "transaction.transactionTotals.totalAmount",
                "ranges": [
                  { "to": 100 },
                  { "from": 100, "to": 500 },
                  { "from": 500, "to": 1000 },
                  { "from": 1000 }
                ]
              }
            }
          }
        ]
      },
      "aggs": {
        "transaction_count": {
          "value_count": {
            "field": "transaction.transactionId.keyword"
          }
        },
        "by_source": {
          "terms": {
            "field": "transaction.source.keyword"
          }
        }
      }
    }
  }
}
```

## 17. Advanced Inventory Analysis (Based on SOLR Query #25)
Demonstrates inventory analysis with nested aggregations.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {
          "nested": {
            "path": "transactionDetails",
            "query": {
              "bool": {
                "must": [
                  { "term": { "transactionDetails.itemType.keyword": "PRODUCT" }}
                ]
              }
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "inventory": {
      "nested": {
        "path": "transactionDetails",
        "aggs": {
          "by_sku": {
            "terms": {
              "field": "transactionDetails.itemSku.keyword",
              "size": 10,
              "order": {
                "total_quantity": "desc"
              }
            },
            "aggs": {
              "total_quantity": {
                "sum": {
                  "field": "transactionDetails.quantity"
                }
              },
              "total_revenue": {
                "sum": {
                  "field": "transactionDetails.lineTotal"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 18. Advanced Fraud Detection (Based on SOLR Query #26)
Demonstrates fraud detection patterns with multiple criteria.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.transactionAdditionalInfo.riskFactor.keyword": "highRisk" }},
        {
          "range": {
            "transaction.transactionTotals.totalAmount": {
              "gte": 1000
            }
          }
        }
      ],
      "should": [
        { "term": { "transaction.source.keyword": "DIGITAL" }},
        { "term": { "transaction.source.keyword": "MOBILE" }}
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "fraud_patterns": {
      "composite": {
        "sources": [
          {
            "by_source": {
              "terms": {
                "field": "transaction.source.keyword"
              }
            }
          },
          {
            "by_payment": {
              "terms": {
                "field": "paymentMethods.paymentType.keyword"
              }
            }
          }
        ]
      },
      "aggs": {
        "total_amount": {
          "sum": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "transaction_count": {
          "value_count": {
            "field": "transaction.transactionId.keyword"
          }
        }
      }
    }
  }
}
```

## 19. Advanced Customer Journey Analysis (Based on SOLR Query #27)
Demonstrates customer journey analysis with time-based patterns.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.clientInfo.clientType.keyword": "REGULAR" }}
      ]
    }
  },
  "aggs": {
    "customer_journey": {
      "terms": {
        "field": "transaction.clientInfo.clientId.keyword",
        "size": 10
      },
      "aggs": {
        "transaction_sequence": {
          "date_histogram": {
            "field": "transaction.transactionDate",
            "calendar_interval": "day"
          },
          "aggs": {
            "by_type": {
              "terms": {
                "field": "transaction.transactionType.keyword"
              }
            },
            "total_amount": {
              "sum": {
                "field": "transaction.transactionTotals.totalAmount"
              }
            }
          }
        }
      }
    }
  }
}
```

## 20. Advanced Performance Metrics (Based on SOLR Query #28)
Demonstrates comprehensive performance metrics with multiple dimensions.
```
GET transaction_history/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "term": { "transaction.transactionType.keyword": "SALE" }}
      ]
    }
  },
  "aggs": {
    "performance_metrics": {
      "composite": {
        "sources": [
          {
            "by_region": {
              "terms": {
                "field": "transaction.transactionAdditionalInfo.region.keyword"
              }
            }
          },
          {
            "by_source": {
              "terms": {
                "field": "transaction.source.keyword"
              }
            }
          }
        ]
      },
      "aggs": {
        "total_sales": {
          "sum": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "transaction_count": {
          "value_count": {
            "field": "transaction.transactionId.keyword"
          }
        },
        "avg_transaction_value": {
          "avg": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "by_status": {
          "terms": {
            "field": "transaction.transactionStatusDesc.keyword"
          }
        }
      }
    },
    "daily_trend": {
      "date_histogram": {
        "field": "transaction.transactionDate",
        "calendar_interval": "day"
      },
      "aggs": {
        "total_sales": {
          "sum": {
            "field": "transaction.transactionTotals.totalAmount"
          }
        },
        "transaction_count": {
          "value_count": {
            "field": "transaction.transactionId.keyword"
          }
        }
      }
    }
  }
}
```

Each query demonstrates specific OpenSearch capabilities:
- Term-level queries for exact matches
- Full-text search with highlighting and fuzzy matching
- Date range queries with histogram aggregations
- Nested queries for complex objects
- Advanced aggregations (terms, date histogram, composite, nested)
- Boolean combinations (must, should, minimum_should_match)
- Field boosting and scoring
- Source filtering
- Highlighting for search results
- Composite aggregations for complex analytics
- Multiple aggregation levels and metrics
- Time-based trend analysis
- Payment method analysis
- Risk factor analysis
- Shipping status tracking
- Loyalty program metrics
- Transaction origin analysis
- Price range analysis with multiple aggregations
- Nested item analysis with quantity and revenue metrics
- Employee performance tracking
- Location-based analytics
- Discount analysis with nested aggregations
- Customer segmentation with composite aggregations
- Inventory analysis with SKU-level metrics
- Fraud detection patterns
- Customer journey analysis
- Comprehensive performance metrics 