# advanced_api_project — DRF Generic Views

## Endpoints
- `GET  /api/books/` — list (public)
- `GET  /api/books/<pk>/` — detail (public)
- `POST /api/books/create/` — create (authenticated)
- `PATCH/PUT /api/books/<pk>/update/` — update (authenticated)
- `DELETE /api/books/<pk>/delete/` — delete (authenticated)

## Permissions
- Read: public (AllowAny)
- Write: authenticated users only (IsAuthenticated)

## Filters
- List supports `?search=<title>` and `?ordering=title` or `?ordering=-publication_year`

## Notes
- Custom validation lives in `BookSerializer` (`publication_year` cannot be in the future).
- Views customize `perform_create` / `perform_update` hooks for extensibility.
