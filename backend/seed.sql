INSERT INTO projects (title, description, tech_stack, repo_url, demo_url, display_order) VALUES
('Budgetrix', 'Comprehensive expense tracking and financial modeling platform with real-time data visualization.', '["React", "Node.js", "MongoDB"]', '#', '#', 1),
('Grocery Dashboard', 'Automated financial reporting and inventory tracking system built for NGO logistics.', '["Python", "Flask", "Excel API"]', '#', '#', 2),
('Silent Bridge', 'Real-time ISL voice translation interface utilizing Web Speech API and animated avatars.', '["JavaScript", "Web Speech", "WebGL"]', '#', '#', 3)
ON DUPLICATE KEY UPDATE title=VALUES(title), description=VALUES(description), tech_stack=VALUES(tech_stack), display_order=VALUES(display_order);
