// ===== User & Authentication Types =====

export type UserRole = 'admin' | 'family' | 'viewer' | 'guest';

export interface User {
  user_id: string; // UUID
  username: string;
  email: string;
  password_hash: string;
  role: UserRole;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface Session {
  session_id: string; // UUID
  user_id: string;
  session_token: string;
  expires_at: Date;
  created_at: Date;
}

// ===== Book Types =====

export interface Book {
  book_id: number;
  composite_id: string;
  title: string;
  subtitle?: string | null;
  publisher?: string | null;
  place_of_publication?: string | null;
  publication_year?: number | null;
  edition?: string | null;
  pages?: number | null;
  isbn?: string | null;
  format_original?: string | null;
  format_expanded?: string | null;
  condition?: string | null;
  copies?: number | null;
  illustrations?: string | null;
  packaging?: string | null;
  topic_id?: number | null;
  is_translation: boolean;
  original_language?: string | null;
  is_multivolume: boolean;
  series_title?: string | null;
  total_volumes?: number | null;
  created_at: Date;
  updated_at: Date;
}

// For single book detail page
export interface BookDetail extends Book {
  topic?: {
    topic_id: number;
    topic_name: string;
  };

  people: Array<{
    person_id: number;
    unified_id: string;
    display_name?: string | null;
    family_name?: string | null;
    given_names?: string | null;
    name_particles?: string | null;
    single_name?: string | null;
    is_organisation?: boolean | null;
    is_author: boolean;
    is_editor: boolean;
    is_contributor: boolean;
    is_translator: boolean;
    sort_order?: number | null;
  }>;

  prices: Array<{
    price_id: number;
    amount: number;
    source?: string | null;
    imported_price?: boolean | null;
    date_added: Date;
  }>;

  volumes?: Array<{
    volume_id: number;
    volume_number?: number | null;
    volume_title?: string | null;
    pages?: number | null;
    notes?: string | null;
  }>;

  admin_data?: {
    original_entry: string;
    needs_review: boolean;
    parsing_confidence?: string | null;
    verification_notes?: string | null;
  };
}

export interface BookWithRelations extends Book {
  topic?: Topic;
  authors: Books2People[];
  editors: Books2People[];
  contributors: Books2People[];
  translator?: Books2People;
  prices: Price[];
  volumes: Volume[];
  admin_data?: BookAdmin;
}

export interface BookDisplayRow {
  // From books table (b.*)
  book_id: number;
  composite_id: string;
  title: string;
  subtitle?: string | null;
  publisher?: string | null;
  place_of_publication?: string | null;
  publication_year?: number | null;
  edition?: string | null;
  pages?: number | null;
  isbn?: string | null;
  format_original?: string | null;
  format_expanded?: string | null;
  condition?: string | null;
  copies?: number | null;
  illustrations?: string | null;
  packaging?: string | null;
  topic_id?: number | null;
  is_translation: boolean;
  original_language?: string | null;
  is_multivolume: boolean;
  series_title?: string | null;
  total_volumes?: number | null;
  book_created_at: Date;
  book_updated_at: Date;

  // From book_admin table (ba.*)
  original_entry?: string | null;
  parsing_confidence?: string | null;
  needs_review?: boolean | null;
  verification_notes?: string | null;
  topic_changed?: boolean | null;
  price_changed?: boolean | null;
  batch_id?: string | null;
  admin_created_at?: Date | null;

  // From topics table (t.*)
  topic_name?: string | null;
  topic_created_at?: Date | null;

  people: Array<{
    person_id: number;
    family_name?: string | null;
    given_names?: string | null;
    name_particles?: string | null;
    single_name?: string | null;
    display_name?: string | null;
    is_author: boolean;
    is_editor: boolean;
    is_contributor: boolean;
    is_translator: boolean;
  }>;

  // From people table (p.*)
  person_id?: number | null;
  unified_id?: string | null;
  family_name?: string | null;
  given_names?: string | null;
  name_particles?: string | null;
  single_name?: string | null;
  is_organisation?: boolean | null;
  person_created_at?: Date | null;
  person_updated_at?: Date | null;

  // From books2people table (b2p.*)
  b2p_id?: number | null;
  display_name?: string | null;
  sort_order?: number | null;
  is_author?: boolean | null;
  is_editor?: boolean | null;
  is_contributor?: boolean | null;
  is_translator?: boolean | null;
  b2p_created_at?: Date | null;
  b2p_updated_at?: Date | null;

  // From prices table (pr.*)
  price_id?: number | null;
  amount?: number | null;
  imported_price?: boolean | null;
  price_source?: string | null;
  price_date_added?: Date | null;

  // From volumes table (b2v.*)
  volume_id?: number | null;
  volume_number?: number | null;
  volume_title?: string | null;
  volume_pages?: number | null;
  volume_notes?: string | null;
}

// ===== People Types =====

export interface Person {
  person_id: number;
  unified_id: string;
  family_name?: string | null;
  given_names?: string | null;
  name_particles?: string | null;
  single_name?: string | null;
  is_organisation: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface Books2People {
  b2p_id: number;
  book_id: number;
  composite_id: string;
  person_id: number;
  unified_id: string;
  display_name?: string | null;
  family_name?: string | null;
  given_names?: string | null;
  name_particles?: string | null;
  single_name?: string | null;
  sort_order?: number | null;
  is_author: boolean;
  is_editor: boolean;
  is_contributor: boolean;
  is_translator: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface PersonWithBooks extends Person {
  books: BookWithRelations[];
  book_count: number;
}

// ===== Topic Types =====

export interface Topic {
  topic_id: number;
  topic_name: string;
  created_at: Date;
}

export interface TopicWithCount extends Topic {
  book_count: number;
}

// ===== Price Types =====

export interface Price {
  price_id: number;
  book_id: number;
  amount: number;
  imported_price: boolean;
  source?: string | null;
  date_added: Date;
}

// ===== Volume Types =====

export interface Volume {
  volume_id: number;
  book_id: number;
  volume_number?: number | null;
  volume_title?: string | null;
  pages?: number | null;
  notes?: string | null;
}

// ===== Book Admin Types =====

export interface BookAdmin {
  book_id: number;
  composite_id: string;
  original_entry: string;
  parsing_confidence?: string | null;
  needs_review: boolean;
  verification_notes?: string | null;
  topic_changed: boolean;
  price_changed: boolean;
  batch_id?: string | null;
  created_at: Date;
}

// ===== API Response Types =====

export interface PaginatedResponse<T> {
  data: T[];
  pagination: PaginationInfo;
}

export type PaginationInfo = {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
};

export interface ApiError {
  error: string;
  message: string;
  status: number;
}

export interface ApiSuccess<T = unknown> {
  success: boolean;
  data?: T;
  message?: string;
}

// ===== Form/Input Types =====

export interface CreateBookInput {
  title: string;
  subtitle?: string;
  publisher?: string;
  place_of_publication?: string;
  publication_year?: number;
  edition?: string;
  pages?: number;
  isbn?: string;
  format_original?: string;
  format_expanded?: string;
  condition?: string;
  copies?: number;
  illustrations?: string;
  packaging?: string;
  topic_id?: number;
  is_translation?: boolean;
  original_language?: string;
  is_multivolume?: boolean;
  series_title?: string;
  total_volumes?: number;
  authors?: CreatePersonInput[];
  editors?: CreatePersonInput[];
  contributors?: CreatePersonInput[];
  translator?: CreatePersonInput;
}

export interface UpdateBookInput extends Partial<CreateBookInput> {
  book_id: number;
}

export interface CreatePersonInput {
  family_name?: string;
  given_names?: string;
  name_particles?: string;
  single_name?: string;
  is_organisation?: boolean;
}

export interface CreatePriceInput {
  book_id: number;
  amount: number;
  source?: string;
}

// ===== Search/Filter Types =====

export interface BookFilters {
  search?: string; // Full-text search across title, authors
  topic_id?: number;
  author?: string; // Filter by author name
  publication_year_min?: number;
  publication_year_max?: number;
  publisher?: string;
  is_translation?: boolean;
  page?: number;
  limit?: number;
}

export interface PeopleFilters {
  search?: string;
  role?: 'author' | 'editor' | 'contributor' | 'translator';
  is_organisation?: boolean;
  page?: number;
  limit?: number;
}
