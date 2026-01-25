# GA4 Event Mapping for VisaFact Checker

This document defines GA4 events and parameters to track the compliance checker funnel and affiliate journey.

## Events

| Event name       | Required params                       | When it fires                                                            |
|------------------|---------------------------------------|--------------------------------------------------------------------------|
| `select_visa`    | `visa_id`                             | User selects a visa route in the checker                                 |
| `select_product` | `product_id`                          | User selects/changes insurance product                                   |
| `run_check`      | `visa_id`, `product_id`, `status`     | User clicks “Check compliance” and receives result (GREEN/YELLOW/RED/UNKNOWN/NOT_REQUIRED) |
| `open_evidence`  | `source_id`                           | User opens an evidence link from results                                 |
| `open_snapshot`  | `snapshot_id`                         | User opens snapshot detail modal/link                                    |
| `copy_link`      | `url`                                 | User copies deep link to share                                           |
| `click_affiliate`| `product_id`, `url`                   | User clicks outbound affiliate link                                      |
| `notify_changes` | `visa_id`                             | User requests notification when snapshot updates (future feature)        |

## Implementation notes
- Use GTM where possible; name parameters exactly as above.
- Include `status` categorical value for funnel segmentation.
- Emit events only after user intent (debounce change listeners).
- Respect consent (EU/EEA): gate firing on consent stored (reuse cookie banner logic).
- No PII should be sent.

## Reporting slices
- Funnel: select_visa → select_product → run_check → click_affiliate.
- Status mix over time to detect data drift.
- Evidence engagement: open_evidence / open_snapshot per session.
- Product/visa breakdown to find underserved routes.

## Testing checklist
- GTM preview shows each event with params.
- GA4 Realtime receives events with correct names/params.
- Events still fire after page reloads and with JS disabled? (document fallback if not).
