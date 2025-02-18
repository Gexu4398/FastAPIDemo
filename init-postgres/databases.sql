create database test encoding 'UTF8' locale_provider 'icu' icu_locale 'zh-u-co-gb2312' template template0;

\c test;

-- 创建序列
CREATE SEQUENCE IF NOT EXISTS city_seq;
CREATE SEQUENCE IF NOT EXISTS district_seq;
CREATE SEQUENCE IF NOT EXISTS population_seq;

-- 城市表
CREATE TABLE IF NOT EXISTS city (
    id BIGINT DEFAULT nextval('city_seq') PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    province VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 区域表
CREATE TABLE IF NOT EXISTS district (
    id BIGINT DEFAULT nextval('district_seq') PRIMARY KEY,
    city_id BIGINT REFERENCES city(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    area_size DECIMAL(10,2), -- 面积（平方公里）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 人口统计表
CREATE TABLE IF NOT EXISTS population_stats (
    id BIGINT DEFAULT nextval('population_seq') PRIMARY KEY,
    city_id BIGINT REFERENCES city(id) ON DELETE CASCADE,
    year INT NOT NULL,
    total_population INT NOT NULL,
    urban_population INT,
    rural_population INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为所有表添加更新时间触发器
CREATE TRIGGER update_city_updated_at
    BEFORE UPDATE ON city
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_district_updated_at
    BEFORE UPDATE ON district
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_population_stats_updated_at
    BEFORE UPDATE ON population_stats
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
