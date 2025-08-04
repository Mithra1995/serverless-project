# 🛍️ Serverless E-Commerce Order Processing System on AWS

A secure, scalable, and cost-efficient e-commerce order management system built entirely using **serverless AWS services**, with a full web-based UI, API layer, database backend, and protection via AWS WAF.

---

## 📌 Live Demo

Frontend: [https://d3h33nn8b5qupv.cloudfront.net/index.html](https://d3h33nn8b5qupv.cloudfront.net/index.html)

---

## 🔗 GitHub Repository

> https://github.com/Mithra1995/serverless-project

---

## 🎯 Objective

To develop a fully serverless e-commerce web application that allows users to:
- Browse products
- Add items to a cart
- Place orders  
All backed by **Lambda**, **API Gateway**, **DynamoDB**, **S3**, and **CloudFront**, with integrated **AWS WAF** for security.

---

## 🏗️ Architecture Overview

| Component           | AWS Service                     |
|--------------------|----------------------------------|
| Frontend UI        | Amazon S3 (Static Website), CloudFront |
| Backend API        | Amazon API Gateway               |
| Business Logic     | AWS Lambda                       |
| Database           | Amazon DynamoDB                  |
| Image Storage      | Amazon S3                        |
| Security           | AWS WAF for CloudFront & API Gateway |


---

## ✨ Features

- 📦 Product listing UI with images
- 🛒 Add to cart functionality
- 🧾 Order placement with live database updates
- 🔒 Secured API endpoints using AWS WAF
- 🚀 Hosted UI with CloudFront CDN
- 🗃️ Data stored in DynamoDB
- 🌐 CORS enabled for cross-origin communication

---

## 🛠️ Step-by-Step Implementation

### 1. Lambda Functions
- `listProductsLambda`: Fetch all product data
- `addToCartLambda`: Add or update items in cart
- `placeOrderLambda`: Finalize order and empty the cart

### 2. IAM Permissions
- Assigned fine-grained permissions for DynamoDB access
- Lambda roles restricted to only necessary actions (PutItem, GetItem, Query, DeleteItem)

### 3. DynamoDB Tables
- `Products` — `product_id`, `name`, `price`, `image_url`
- `Cart` — `user_id`, `product_id`, `quantity`, `total_price`
- `Orders` — `order_id`, `user_id`, `items`, `address`, `timestamp`

### 4. S3 for Images & UI
- Product images stored in one S3 bucket
- Frontend files (`index.html`, `app.js`) stored in a separate bucket with Static Website Hosting enabled

### 5. API Gateway
- Created REST APIs to expose Lambda functions
- Configured CORS for all endpoints
- Deployed stage as `Prod`

### 6. CloudFront
- Integrated with S3 for frontend distribution
- Used **Origin Access Control (OAC)** to restrict S3 access to CloudFront only

### 7. Frontend Integration
- Fetch product list via `/products` API
- Add items to cart with `/cart` API
- Place order via `/order` API
- Cart auto-clears after order
- Real-time updates in DynamoDB verified

### 8. AWS WAF Integration
- Enabled WAF for:
  - CloudFront (global scope)
  - API Gateway (regional scope)
- Added free managed rule sets (SQLi, XSS, bad bots, etc.)
- Monitored traffic and threats in AWS WAF dashboard

---

## ⚠️ Security

- Used **AWS WAF** to protect both CloudFront and API Gateway endpoints.
- Disabled S3 public access and routed all access through CloudFront.
- CORS enabled only for required endpoints.
- IAM roles follow the principle of least privilege.

---

## 🚀 How to Deploy This Project (Optional Section)

1. Clone the repo
2. Create DynamoDB tables and insert sample product data
3. Create 3 Lambda functions and attach IAM roles
4. Set up API Gateway endpoints and enable CORS
5. Upload frontend files and images to S3
6. Create CloudFront distribution for frontend bucket
7. Add WAF to CloudFront and API Gateway
8. Test complete e-commerce flow

---

## 📦 Technologies Used

- **AWS Lambda**
- **Amazon API Gateway**
- **Amazon DynamoDB**
- **Amazon S3**
- **Amazon CloudFront**
- **AWS WAF**
- **JavaScript, HTML, CSS (for frontend)**

---

## 👨‍💻 Author

**Mithra Balasubramaniam**

- GitHub: [Mithra1995](https://github.com/Mithra1995)

---
