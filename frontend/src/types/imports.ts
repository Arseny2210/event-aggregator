export type ImportStatus = "processing" | "completed" | "failed"

export type ImportRowStatus = "imported" | "warning" | "failed"

export interface ImportSummary {
  total_rows: number
  processed_rows: number
  imported_rows: number
  failed_rows: number
  warning_rows: number
  duration: number
  started_at?: string
  finished_at?: string
  progress_percent: number
}

export interface ImportJob {
  id: string
  filename: string
  status: ImportStatus
  created_by: string
  created_at: string
  summary: ImportSummary
}

export interface RowResult {
  id: string
  import_job_id: string
  row_number: number
  status: ImportRowStatus
  created_entity_id?: string
  error_code?: string
  error_message?: string
  created_at: string
}

export interface ImportListParams {
  offset?: number
  limit?: number
  status?: ImportStatus
}

export interface RowResultParams {
  offset?: number
  limit?: number
  status?: ImportRowStatus
}

export const IMPORT_STATUS_LABELS: Record<ImportStatus, string> = {
  processing: "Processing",
  completed: "Completed",
  failed: "Failed",
}

export const IMPORT_STATUS_COLORS: Record<ImportStatus, string> = {
  processing: "bg-blue-100 text-blue-700",
  completed: "bg-green-100 text-green-700",
  failed: "bg-red-100 text-red-700",
}

export const IMPORT_ROW_STATUS_LABELS: Record<ImportRowStatus, string> = {
  imported: "Imported",
  warning: "Warning",
  failed: "Failed",
}

export const IMPORT_ROW_STATUS_COLORS: Record<ImportRowStatus, string> = {
  imported: "bg-green-100 text-green-700",
  warning: "bg-amber-100 text-amber-700",
  failed: "bg-red-100 text-red-700",
}
