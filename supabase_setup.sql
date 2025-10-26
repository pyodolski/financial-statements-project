-- Supabase 테이블 생성 SQL
-- Supabase 대시보드의 SQL Editor에서 실행하세요

CREATE TABLE IF NOT EXISTS income_statements (
    id BIGSERIAL PRIMARY KEY,
    upload_filename TEXT NOT NULL,
    input_file_path TEXT NOT NULL,
    output_file_path TEXT NOT NULL,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    total_sales NUMERIC(15, 2) NOT NULL,
    total_cost NUMERIC(15, 2) NOT NULL,
    gross_profit NUMERIC(15, 2) NOT NULL,
    deposit_amount NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_upload_date ON income_statements(upload_date DESC);

-- Row Level Security (RLS) 활성화 (선택사항)
ALTER TABLE income_statements ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽을 수 있도록 정책 생성 (선택사항)
CREATE POLICY "Enable read access for all users" ON income_statements
    FOR SELECT USING (true);

-- 모든 사용자가 삽입할 수 있도록 정책 생성 (선택사항)
CREATE POLICY "Enable insert access for all users" ON income_statements
    FOR INSERT WITH CHECK (true);
