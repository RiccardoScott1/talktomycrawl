-- Enable the pgvector extension to work with embedding vectors
create extension vector;

-- Create a table to store page dats
drop table if exists crawled_pages;
create table crawled_pages (
  url text,
  created_at TIMESTAMP DEFAULT NOW(),
  links jsonb,
  metadata jsonb,
  markdown text,
  html text,
  cleaned_html text
);


-- Create a table to store your documents
drop table if exists documents;
create table documents (
  id bigserial primary key,
  content text, -- corresponds to Document.pageContent
  metadata jsonb, -- corresponds to Document.metadata
  embedding vector(768) -- 768 is the dimension of the embedding
);

-- Create a function to search for documents
create function match_documents (
  query_embedding vector(768),
  match_count int default null,
  filter jsonb DEFAULT '{}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;