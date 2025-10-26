-- 기존 테이블에 transaction_period 컬럼 추가
-- Supabase 대시보드의 SQL Editor에서 실행하세요

ALTER TABLE income_statements ADD COLUMN IF NOT EXISTS transaction_period TEXT;

-- 인덱스 추가 (거래기간으로 검색 최적화)
CREATE INDEX IF NOT EXISTS idx_transaction_period ON income_statements(transaction_period);
