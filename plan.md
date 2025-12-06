# UI Enhancements Plan: Button Refinements & Focus Styling

## Overview
This plan implements UI enhancements for the TimeTracker4 TUI application:
1. Make existing buttons slightly smaller
2. Add an Exit button (same style as other buttons)
3. Align the button row within the frame
4. Change button focus appearance from text highlighting to border highlighting

## Implementation Approach

### Part 1: Button Size & Exit Button

**Strategy:** Reduce button width, add Exit button to the existing button container, and ensure proper alignment within the frame.

**Current Button Layout (in compose()):**
```python
Container(
    Button("Start", id="start-stop-btn", variant="success"),
    Button("Reports", id="reports-btn"),
    id="button-container"
)
```

**New Button Layout:**
```python
Container(
    Button("Start", id="start-stop-btn", variant="success"),
    Button("Reports", id="reports-btn"),
    Button("Exit", id="exit-btn"),
    id="button-container"
)
```

**Implementation Steps:**

1. **Modify `src/ui/screens/main_screen.py`:**

   a. Update `compose()` method (lines 33-55):
   - Add Exit button to the button container (after Reports button):
   ```python
   Button("Exit", id="exit-btn"),
   ```

   b. Extend `on_button_pressed()` method (lines 90-95):
   - Add handler for exit button:
   ```python
   elif event.button.id == "exit-btn":
       self.app.action_quit()
   ```

2. **Update CSS styling in `src/styles.css`:**

   a. Modify button sizing (around line 66-70):
   - Change button `min-width` from current value to smaller value (e.g., 10 or 9):
   ```css
   #button-container Button {
       min-width: 10;  /* Reduced from previous value */
       margin: 0 1;
   }
   ```

   b. Add proper centering to button-container (around line 60-64):
   ```css
   #button-container {
       width: 100%;
       height: auto;
       align: center middle;
       layout: horizontal;
   }
   ```

**Design Decisions:**
- **Button Size:** Slightly reduce `min-width` to make buttons more compact
- **Exit Button:** Same style as existing buttons for consistency
- **Alignment:** Use Textual's `align: center middle` to center the button row horizontally within the frame
- **Variant:** Exit button uses default variant (not error) to match Reports button styling

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
- Lines 33-55: Add Exit button to `compose()` method's button container
- Lines 90-95: Extend `on_button_pressed()` with exit button handler

### 2. `/home/mike/projects/timetracker4/src/styles.css`
- Lines 60-70: Update `#button-container` styling for alignment and button sizing
- After line 112: Add button focus styling rules

## Testing Approach

**Manual verification steps:**

1. **Button Layout Tests:**
   - [ ] Buttons appear smaller (reduced width)
   - [ ] Exit button appears after Reports button
   - [ ] Button row is centered within the frame
   - [ ] Layout remains compact and aligned
   - [ ] All three buttons are consistently sized

2. **Exit Button Tests:**
   - [ ] Exit button appears with default styling (matches Reports button)
   - [ ] Clicking Exit button exits the application
   - [ ] Exit button is included in tab navigation

3. **Focus Styling Tests:**
   - [ ] Tab key cycles through all widgets (including Exit button)
   - [ ] Focused buttons show border (not text highlighting)
   - [ ] "Start" button shows green border when focused
   - [ ] "Stop" button shows red border when focused (after starting tracking)
   - [ ] "Reports" and "Exit" buttons show primary color border when focused
   - [ ] No layout shift when buttons gain/lose focus

4. **Integration Tests:**
   - [ ] 'q' keyboard shortcut still works
   - [ ] 's' keyboard shortcut still works
   - [ ] Starting/stopping tracking updates button variant and focus border color
   - [ ] Button alignment remains correct when Start changes to Stop

## Implementation Sequence

**Recommended order:**

1. **Phase 1:** Button focus styling (lower risk)
   - Add focus CSS rules to `src/styles.css`
   - Test with Tab key navigation
   - Verify no layout issues

2. **Phase 2:** Exit button and sizing (moderate complexity)
   - Update button container CSS for alignment and sizing
   - Add Exit button to `compose()` method
   - Add exit button handler to `on_button_pressed()`
   - Test button layout, sizing, and functionality

This sequence allows testing focus styling independently before modifying the button layout.

## Potential Issues & Mitigation

**Issue:** Three buttons might not fit properly within the frame width
- **Mitigation:** Reduce button `min-width` to accommodate all three buttons; test various terminal sizes

**Issue:** Focus border might cause layout shift
- **Mitigation:** Pre-allocate border space with `border: solid transparent` in default state

**Issue:** Button variant changes might not update focus border color
- **Mitigation:** Textual's reactive CSS should handle this automatically; test during start/stop transitions

**Issue:** Button row might not appear centered
- **Mitigation:** Use `align: center middle` in CSS and verify horizontal centering with different button states

## Dependencies

- No new dependencies required
- Uses existing Textual widgets and features
- Textual version ≥0.47.0 (already satisfied)
