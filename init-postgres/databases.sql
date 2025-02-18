create database test encoding 'UTF8' locale_provider 'icu' icu_locale 'zh-u-co-gb2312' template template0;

\c test;
CREATE TABLE city
(
    id   BIGINT       NOT NULL PRIMARY KEY,
    name VARCHAR(256) NOT NULL
);

CREATE SEQUENCE city_seq MAXVALUE 9223372036854775807 NO CYCLE;


