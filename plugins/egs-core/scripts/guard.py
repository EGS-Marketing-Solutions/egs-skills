#!/usr/bin/env python3
"""PreToolUse guard for the egs-core plugin. Keeps every EGS Claude read-only in EGS's tools, and keeps
Claude out of the person's secrets files. Prints a deny decision for blocked calls; prints nothing otherwise."""
import json, re, sys

WRITE_TOOLS = re.compile(
    r"^mcp__claude_ai_Gmail__(send_message|reply|forward|create_draft|update_draft|delete_draft|trash_.*|untrash_.*|"
    r"label_.*|unlabel_.*|update_message_labels|create_label|delete_label|update_label|mark_.*|unmark_.*|apply_.*)$"
    r"|^mcp__claude_ai_Google_Drive__(create_file|update_file|copy_file|share_file|trash_file)$"
    r"|^mcp__claude_ai_Google_Calendar__.*(create|update|delete|respond|move).*$"
    r"|^mcp__claude_ai_Meta_Ads__ads_(create|update|delete|activate|boost|catalog_(create|update|delete|product_create)|"
    r"creative_(create|update|delete|upload)|experiment_.*_(create|update)|pixel_.*_(create|update|delete)|"
    r"finalize_.*|delete_.*|log_ui_interaction).*$"
    r"|^mcp__claude_ai_Canva__(create|edit|generate|copy|merge|resize|move|comment|reply|upload|autofill|publish|import|"
    r"remove|separate).*$"
    r"|^mcp__claude_ai_Slack__.*(send|post|update|delete|add|react|create|schedule|invite|archive).*$"
    r"|^mcp__claude_ai_Fathom__$")
WRITE_VERBS = re.compile(r"(create|update|delete|publish|send|remove|cancel|upsert|archive|merge|import|bulk|add|post|put|patch)", re.I)
SECRETS = re.compile(r"egs-assistant[/\\](plutio\.json|google-token\.json|google-client\.json|pagespeed\.json)")


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        return
    tool = data.get("tool_name", "")
    args = data.get("tool_input") or {}
    if WRITE_TOOLS.search(tool):
        return deny("The EGS skills are read-only: Claude does not send, post or change anything in EGS's tools. "
                    "Write the text for the person to send or post themselves.")
    if tool.endswith("__execute_operation") and WRITE_VERBS.search(json.dumps(args)[:400]):
        return deny("Amplify is read-only for the EGS skills. Write the build spec; a person makes the change.")
    if tool in ("Read", "Bash") and SECRETS.search(json.dumps(args)):
        return deny("That file holds the person's private keys. Claude never opens it.")


if __name__ == "__main__":
    main()
