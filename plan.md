# UI Enhancements Plan: Close Button & Button Focus Styling

## Overview
This plan implements two UI enhancements for the TimeTracker4 TUI application:
1. Add a red X close button in the top-right corner of the Time Tracker frame
2. Change button focus appearance from text highlighting to border highlighting

## Implementation Approach

### Part 1: Red X Close Button

**Strategy:** Add a horizontal container at the top of the main screen that holds both the title and a small close button.

**Layout Structure:**
```
Vertical (main-container)
├── Horizontal (title-bar) ← NEW
│   ├── Static (title) - centered, takes remaining space
│   └── Button (close-btn) - red X, fixed width, aligned right
├── Static (status-display)
├── Static (project-display)
... rest of content
```

**Implementation Steps:**

1. **Modify `src/ui/screens/main_screen.py`:**

   a. Add `Horizontal` import (line 6):
   ```python
   from textual.containers import Container, Vertical, Horizontal
   ```

   b. Update `compose()` method (lines 33-55):
   - Replace `Static("Time Tracker", id="title")` with:
   ```python
   Horizontal(
       Static("Time Tracker", id="title"),
       Button("X", id="close-btn", variant="error", can_focus=False),
       id="title-bar"
   ),
   ```

   c. Extend `on_button_pressed()` method (lines 90-95):
   - Add handler for close button:
   ```python
   elif event.button.id == "close-btn":
       self.app.action_quit()
   ```

2. **Add CSS styling to `src/styles.css`:**

   Insert after line 35 (after `#title` section):
   ```css
   /* Title bar - horizontal container for title + close button */
   #title-bar {
       height: auto;
       width: 100%;
   }

   /* Override title styling when inside title-bar */
   #title-bar #title {
       width: 1fr;
       text-align: center;
       text-style: bold;
       color: $accent;
       margin-bottom: 0;
   }

   /* Close button styling */
   #close-btn {
       width: 3;
       min-width: 3;
       height: 1;
       padding: 0;
       margin-left: auto;
       background: $error;
       color: $text;
   }

   #close-btn:hover {
       text-style: bold;
   }
   ```

**Design Decisions:**
- **Scope:** Main screen only (not added to summary/detail screens)
- **Widget:** Button (not Static) for built-in click handling and accessibility
- **Character:** Simple "X" for maximum terminal compatibility
- **Focusable:** `can_focus=False` to keep it out of tab navigation (since 'q' key provides keyboard access)
- **Size:** Minimal (width: 3, height: 1) to be unobtrusive
- **Color:** `variant="error"` for red background matching the error theme

### Part 2: Button Focus Border Styling

**Strategy:** Use CSS pseudo-selectors to override Textual's default focus behavior, replacing text highlighting with border highlighting that matches button variant colors.

**Implementation Steps:**

1. **Add CSS rules to `src/styles.css`:**

   Append to end of file (after line 112):
   ```css
   /* Custom button focus styling - use border instead of text highlighting */

   /* Ensure buttons have space for focus border to prevent layout shift */
   #button-container Button {
       margin: 0 1;
       min-width: 12;
       border: solid transparent;  /* Pre-allocate border space */
   }

   /* Base button focus styling */
   Button:focus {
       text-style: none;
   }

   /* Focus borders matching button variants */
   Button:focus {
       border: heavy $primary;
   }

   Button.success:focus {
       border: heavy $success;
       background: $success;
   }

   Button.error:focus {
       border: heavy $error;
       background: $error;
   }
   ```

**Design Decisions:**
- **Border Style:** `heavy` for clear visibility
- **Variant Matching:** Focus border color matches button variant (green for success, red for error)
- **Layout Stability:** Transparent border in default state prevents layout shift when gaining focus
- **Dynamic Behavior:** CSS automatically updates border color when button variant changes (Start→Stop)

## Files to Modify

### 1. `/home/mike/projects/timetracker4/src/ui/screens/main_screen.py`
- Line 6: Add `Horizontal` import
- Lines 33-55: Modify `compose()` to add title-bar and close button
- Lines 90-95: Extend `on_button_pressed()` with close button handler

### 2. `/home/mike/projects/timetracker4/src/styles.css`
- After line 35: Add title-bar and close-btn styling
- After line 112: Add button focus styling rules

### 3. `/home/mike/projects/timetracker4/src/app.py`
- No changes needed (existing quit binding at line 21 will be used)

## Testing Approach

**Manual verification steps:**

1. **Close Button Tests:**
   - [ ] Close button appears in top-right corner inside the frame
   - [ ] Close button is red
   - [ ] Clicking close button exits the application
   - [ ] Title remains visually centered
   - [ ] Layout remains compact (width 45)

2. **Focus Styling Tests:**
   - [ ] Tab key cycles through widgets
   - [ ] Focused buttons show border (not text highlighting)
   - [ ] "Start" button shows green border when focused
   - [ ] "Stop" button shows red border when focused (after starting tracking)
   - [ ] "Reports" button shows primary color border when focused
   - [ ] No layout shift when buttons gain/lose focus

3. **Integration Tests:**
   - [ ] 'q' keyboard shortcut still works
   - [ ] 's' keyboard shortcut still works
   - [ ] Starting/stopping tracking updates button variant and focus border color

## Implementation Sequence

**Recommended order:**

1. **Phase 1:** Button focus styling (lower risk)
   - Add focus CSS rules
   - Test with Tab key navigation
   - Verify no layout issues

2. **Phase 2:** Close button (higher complexity)
   - Add Horizontal import
   - Modify compose() method
   - Add click handler
   - Add CSS styling
   - Test functionality and positioning

This sequence allows testing focus styling independently before introducing layout changes.

## Potential Issues & Mitigation

**Issue:** Title might appear off-center with close button present
- **Mitigation:** Title uses `width: 1fr` to take remaining space with `text-align: center` for visual centering

**Issue:** Focus border might cause layout shift
- **Mitigation:** Pre-allocate border space with `border: solid transparent` in default state

**Issue:** Button variant changes might not update focus border color
- **Mitigation:** Textual's reactive CSS should handle this automatically; test during start/stop transitions

## Dependencies

- No new dependencies required
- Uses existing Textual widgets and features
- Textual version ≥0.47.0 (already satisfied)
