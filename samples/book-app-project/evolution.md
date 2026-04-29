# Evolution: Add Rating & Review Features to Book App

## Problem
The book app tracks books and read status but has no way to rate or review books.

## Approach
- Add optional `rating` (1–5 int) and `review` (str) fields to the `Book` dataclass
- Prompt for rating and optional review text when the user marks a book as read
- Add a `reviews` command to list all rated books with their ratings and reviews
- Update `stats` to include average rating across rated books
- Update `show_books` display to show star rating inline
- Add pytest tests covering all new logic

## Decisions
- **Rating scale**: 1–5 stars
- **Review text**: optional (can rate without a written review)
- **Entry point**: rating/review is collected when marking as read (`handle_mark_read`)
- **Stats**: show average rating (only over books that have been rated)
- **`reviews` command**: lists all rated books with rating + review text

## Files to Change

| File | Change |
|------|--------|
| `books.py` | Add `rating: Optional[int] = None` and `review: Optional[str] = None` to `Book`; add `rate_book()` method to `BookCollection` |
| `book_app.py` | Update `handle_mark_read()` to prompt for rating+review; update `show_books()` to show stars; update `handle_stats()` to show avg rating; add `handle_reviews()` handler and wire to `COMMANDS`; update `show_help()` |
| `data.json` | Add `"rating": null, "review": null` to existing entries (backward-compatible) |
| `tests/test_books.py` | Add tests for `rate_book()`, invalid rating, rating display in stats |

## Implementation Notes
- New optional fields on `Book` are backward-compatible: existing JSON entries without `rating`/`review` load correctly via `None` defaults
- Star display: `★★★☆☆` style using filled/empty star chars
- Validation: rating must be 1–5 (inclusive); anything else prints an error and leaves rating as `None`
- `rate_book(title, rating, review)` on `BookCollection` sets fields and saves

## Tasks

- [ ] Add `rating`/`review` fields to `Book` dataclass + `rate_book()` method (`books.py`)
- [ ] Prompt for rating/review in `handle_mark_read()` (`book_app.py`)
- [ ] Show star rating inline in `show_books()` (`book_app.py`)
- [ ] Add avg rating to `handle_stats()` (`book_app.py`)
- [ ] Add `handle_reviews()` command + wire into `COMMANDS` + `show_help()` (`book_app.py`)
- [ ] Add `"rating": null, "review": null` to existing entries in `data.json`
- [ ] Add pytest tests for new rating/review functionality (`tests/test_books.py`)
