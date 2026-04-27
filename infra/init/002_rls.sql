ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chunks ENABLE ROW LEVEL SECURITY;

CREATE POLICY documents_policy
ON documents
USING (pipeline_id IS NOT NULL);

CREATE POLICY chunks_policy
ON chunks
USING (document_id IS NOT NULL);