CREATE TABLE IF NOT EXISTS sales_orders (
  order_id SERIAL PRIMARY KEY,
  customer_name TEXT NOT NULL,
  campaign_name TEXT,
  amount NUMERIC(12,2) NOT NULL,
  discount_rate NUMERIC(5,2) DEFAULT 0,
  is_promotion BOOLEAN DEFAULT FALSE,
  order_date DATE NOT NULL
);

INSERT INTO sales_orders (customer_name, campaign_name, amount, discount_rate, is_promotion, order_date) VALUES
('客户A', '春季促销', 12000, 0.15, TRUE, CURRENT_DATE - INTERVAL '95 days'),
('客户B', '春季促销', 8000, 0.10, TRUE, CURRENT_DATE - INTERVAL '88 days'),
('客户C', NULL, 15000, 0.00, FALSE, CURRENT_DATE - INTERVAL '78 days'),
('客户D', '暑期大促', 22000, 0.20, TRUE, CURRENT_DATE - INTERVAL '45 days'),
('客户E', NULL, 9000, 0.00, FALSE, CURRENT_DATE - INTERVAL '20 days');
