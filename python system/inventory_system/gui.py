import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Add parent dir to path so imports work when run from gui.py location
sys.path.insert(0, ".")

from utils.service_locator import ServiceLocator


class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("1100x700")
        self.configure(bg="#1e1e2e")
        self.resizable(True, True)

        self.sl = ServiceLocator()
        self.inv = self.sl.inventory_service
        self.txn = self.sl.transaction_service

        self._build_ui()
        self._refresh_table()

    # ─── UI Builder ───────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg="#313244", pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="  Inventory Management System",
                 font=("Segoe UI", 18, "bold"), bg="#313244", fg="#cdd6f4").pack()

        # Main content
        main = tk.Frame(self, bg="#1e1e2e")
        main.pack(fill="both", expand=True, padx=16, pady=10)

        # Left panel – scrollable with all actions
        left_outer = tk.Frame(main, bg="#1e1e2e", width=360)
        left_outer.pack(side="left", fill="both", expand=True, padx=(0, 12))
        left_outer.pack_propagate(False)

        left_canvas = tk.Canvas(left_outer, bg="#1e1e2e", highlightthickness=0, width=360)
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar = tk.Scrollbar(left_outer, orient="vertical", command=left_canvas.yview)
        left_scrollbar.pack(side="right", fill="y")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)

        left = tk.Frame(left_canvas, bg="#1e1e2e")
        left_id = left_canvas.create_window((0, 0), window=left, anchor="nw", width=340)

        def on_left_frame_configure(event):
            left_canvas.configure(scrollregion=left_canvas.bbox("all"))
            left_canvas.itemconfig(left_id, width=left_canvas.winfo_width())
        left.bind("<Configure>", on_left_frame_configure)

        def _on_mousewheel(event):
            left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        left_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Add all main.py actions as sections
        self._build_add_form(left)
        self._build_list_form(left)
        self._build_stock_in_form(left)
        self._build_stock_out_form(left)
        self._build_adjust_form(left)
        self._build_low_stock_form(left)
        self._build_inventory_report_form(left)
        self._build_transaction_ledger_form(left)
        self._build_audit_trail_form(left)

        # Right panel – tables
        right = tk.Frame(main, bg="#1e1e2e")
        right.pack(side="left", fill="both", expand=True)

        self._build_inventory_table(right)
        self._build_transaction_table(right)
    # ─── List Inventory Items ───────────────────────────────────────────────
    def _build_list_form(self, parent):
        frm = self._card(parent, "  List Inventory Items")
        tk.Button(frm, text="List Items", command=self._list_items,
                  **self._btn_style("#b4befe")).pack(fill="x", pady=(8, 0))

    def _list_items(self):
        items = self.inv.get_all_items()
        if not items:
            messagebox.showinfo("Inventory", "No inventory items found.")
            return
        win = tk.Toplevel(self)
        win.title("Inventory Items")
        text = tk.Text(win, width=60, height=20)
        text.pack()
        for item in items:
            text.insert(tk.END, f"• {item.name} ({item.sku}) — Qty: {item.quantity}, Unit Cost: ${item.unit_cost:.2f}\n")
        text.config(state=tk.DISABLED)

    # ─── Stock In Form ─────────────────────────────────────────────────────
    def _build_stock_in_form(self, parent):
        frm = self._card(parent, "  Stock In")
        self._lbl_entry(frm, "SKU *", "si_sku")
        self._lbl_entry(frm, "Quantity *", "si_qty")
        self._lbl_entry(frm, "Reference ID", "si_ref")
        self._lbl_entry(frm, "Performed By", "si_by")
        self._lbl_entry(frm, "Notes", "si_notes")
        tk.Button(frm, text="Stock In", command=self._stock_in_action,
                  **self._btn_style("#89b4fa")).pack(fill="x", pady=(8, 0))

    def _stock_in_action(self):
        sku = getattr(self, "si_sku").get().strip()
        qty = getattr(self, "si_qty").get().strip()
        ref = getattr(self, "si_ref").get().strip() or None
        by = getattr(self, "si_by").get().strip() or None
        notes = getattr(self, "si_notes").get().strip() or None
        if not sku:
            messagebox.showerror("Validation", "SKU is required.")
            return
        try:
            qty = int(qty)
        except ValueError:
            messagebox.showerror("Validation", "Quantity must be an integer.")
            return
        item = self.inv.get_by_sku(sku)
        if not item:
            messagebox.showerror("Error", f"Item with SKU '{sku}' not found.")
            return
        result = self.txn.stock_in(item.id, qty, ref, by, notes)
        if result.success:
            messagebox.showinfo("Success", f"Stock In of {qty} units recorded.")
            self._clear_fields("si_sku", "si_qty", "si_ref", "si_by", "si_notes")
            self._refresh_table()
        else:
            messagebox.showerror("Error", result.error)

    # ─── Stock Out Form ────────────────────────────────────────────────────
    def _build_stock_out_form(self, parent):
        frm = self._card(parent, "  Stock Out")
        self._lbl_entry(frm, "SKU *", "so_sku")
        self._lbl_entry(frm, "Quantity *", "so_qty")
        self._lbl_entry(frm, "Reference ID", "so_ref")
        self._lbl_entry(frm, "Performed By", "so_by")
        self._lbl_entry(frm, "Notes", "so_notes")
        tk.Button(frm, text="Stock Out", command=self._stock_out_action,
                  **self._btn_style("#f38ba8")).pack(fill="x", pady=(8, 0))

    def _stock_out_action(self):
        sku = getattr(self, "so_sku").get().strip()
        qty = getattr(self, "so_qty").get().strip()
        ref = getattr(self, "so_ref").get().strip() or None
        by = getattr(self, "so_by").get().strip() or None
        notes = getattr(self, "so_notes").get().strip() or None
        if not sku:
            messagebox.showerror("Validation", "SKU is required.")
            return
        try:
            qty = int(qty)
        except ValueError:
            messagebox.showerror("Validation", "Quantity must be an integer.")
            return
        item = self.inv.get_by_sku(sku)
        if not item:
            messagebox.showerror("Error", f"Item with SKU '{sku}' not found.")
            return
        result = self.txn.stock_out(item.id, qty, ref, by, notes)
        if result.success:
            messagebox.showinfo("Success", f"Stock Out of {qty} units recorded.")
            self._clear_fields("so_sku", "so_qty", "so_ref", "so_by", "so_notes")
            self._refresh_table()
        else:
            messagebox.showerror("Error", result.error)

    # ─── Low Stock Form ─────────────────────────────────────────────────────
    def _build_low_stock_form(self, parent):
        frm = self._card(parent, "  View Low Stock")
        self._lbl_entry(frm, "Threshold", "ls_threshold")
        tk.Button(frm, text="View Low Stock", command=self._view_low_stock_action,
                  **self._btn_style("#f9e2af")).pack(fill="x", pady=(8, 0))

    def _view_low_stock_action(self):
        threshold = getattr(self, "ls_threshold").get().strip() or "5"
        try:
            threshold = int(threshold)
        except ValueError:
            messagebox.showerror("Validation", "Threshold must be an integer.")
            return
        low_stock = self.inv.get_low_stock(threshold=threshold)
        if not low_stock:
            messagebox.showinfo("Low Stock", "No low stock items.")
            return
        win = tk.Toplevel(self)
        win.title("Low Stock Items")
        text = tk.Text(win, width=60, height=20)
        text.pack()
        for item in low_stock:
            text.insert(tk.END, f"• {item.name} ({item.sku}): {item.quantity} units\n")
        text.config(state=tk.DISABLED)

    # ─── Inventory Report Form ─────────────────────────────────────────────
    def _build_inventory_report_form(self, parent):
        frm = self._card(parent, "  View Inventory Report")
        tk.Button(frm, text="View Inventory Report", command=self._view_inventory_report_action,
                  **self._btn_style("#a6e3a1")).pack(fill="x", pady=(8, 0))

    def _view_inventory_report_action(self):
        items = self.inv.get_all_items()
        win = tk.Toplevel(self)
        win.title("Inventory Report")
        text = tk.Text(win, width=80, height=25)
        text.pack()
        import io, sys
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        from utils.report import ReportUtils
        ReportUtils.print_inventory_report(items)
        sys.stdout = sys_stdout
        text.insert(tk.END, buf.getvalue())
        text.config(state=tk.DISABLED)

    # ─── Transaction Ledger Form ─────────────────────────────────────────--
    def _build_transaction_ledger_form(self, parent):
        frm = self._card(parent, "  View Transaction Ledger")
        self._lbl_entry(frm, "SKU *", "tl_sku")
        tk.Button(frm, text="View Transaction Ledger", command=self._view_transaction_ledger_action,
                  **self._btn_style("#b4befe")).pack(fill="x", pady=(8, 0))

    def _view_transaction_ledger_action(self):
        sku = getattr(self, "tl_sku").get().strip()
        item = self.inv.get_by_sku(sku)
        if not item:
            messagebox.showerror("Error", "Item not found.")
            return
        txns = self.sl.transaction_repo.get_by_item_id(item.id)
        win = tk.Toplevel(self)
        win.title("Transaction Ledger")
        text = tk.Text(win, width=80, height=25)
        text.pack()
        import io, sys
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        from utils.report import ReportUtils
        ReportUtils.print_transaction_ledger(item, txns)
        sys.stdout = sys_stdout
        text.insert(tk.END, buf.getvalue())
        text.config(state=tk.DISABLED)

    # ─── Audit Trail Form ─────────────────────────────────────────────────--
    def _build_audit_trail_form(self, parent):
        frm = self._card(parent, "  View Audit Trail")
        tk.Button(frm, text="View Audit Trail", command=self._view_audit_trail_action,
                  **self._btn_style("#f38ba8")).pack(fill="x", pady=(8, 0))

    def _view_audit_trail_action(self):
        logs = self.sl.audit_log_repo.get_all()
        win = tk.Toplevel(self)
        win.title("Audit Trail")
        text = tk.Text(win, width=80, height=25)
        text.pack()
        import io, sys
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        from utils.report import ReportUtils
        ReportUtils.print_audit_trail(logs)
        sys.stdout = sys_stdout
        text.insert(tk.END, buf.getvalue())
        text.config(state=tk.DISABLED)

    # ─── Add Item Form ────────────────────────────────────────────────────────

    def _build_add_form(self, parent):
        frm = self._card(parent, "  Add Inventory Item")

        self._lbl_entry(frm, "SKU *", "e_sku")
        self._lbl_entry(frm, "Name *", "e_name")
        self._lbl_entry(frm, "Unit Cost *", "e_cost")
        self._lbl_entry(frm, "Initial Qty", "e_qty")
        self._lbl_entry(frm, "Description", "e_desc")
        self._lbl_entry(frm, "Created By", "e_created_by")

        tk.Button(frm, text="Add Item", command=self._add_item,
                  **self._btn_style("#a6e3a1")).pack(fill="x", pady=(8, 0))

    # ─── Stock In / Out Form ──────────────────────────────────────────────────

    def _build_stock_form(self, parent):
        outer = self._card(parent, "  Stock In / Out")
        # Create a scrollable canvas
        canvas = tk.Canvas(outer, bg="#313244", highlightthickness=0, height=220)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        frm = tk.Frame(canvas, bg="#313244")
        canvas.create_window((0, 0), window=frm, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        frm.bind("<Configure>", on_frame_configure)

        self._lbl_entry(frm, "SKU *", "s_sku")
        self._lbl_entry(frm, "Quantity *", "s_qty")
        self._lbl_entry(frm, "Reference ID", "s_ref")
        self._lbl_entry(frm, "Performed By", "s_by")
        self._lbl_entry(frm, "Notes", "s_notes")

        btn_row = tk.Frame(frm, bg="#313244")
        btn_row.pack(fill="x", pady=(8, 0))
        tk.Button(btn_row, text="Stock In", command=self._stock_in,
                  **self._btn_style("#89b4fa")).pack(side="left", fill="x", expand=True, padx=(0, 4))
        tk.Button(btn_row, text="Stock Out", command=self._stock_out,
                  **self._btn_style("#f38ba8")).pack(side="left", fill="x", expand=True)

    # ─── Adjust Form ──────────────────────────────────────────────────────────

    def _build_adjust_form(self, parent):
        frm = self._card(parent, "  Adjust Inventory")

        self._lbl_entry(frm, "SKU *", "a_sku")
        self._lbl_entry(frm, "New Quantity *", "a_qty")
        self._lbl_entry(frm, "Performed By", "a_by")
        self._lbl_entry(frm, "Notes", "a_notes")

        tk.Button(frm, text="Apply Adjustment", command=self._adjust,
                  **self._btn_style("#fab387")).pack(fill="x", pady=(8, 0))

    # ─── Inventory Table ──────────────────────────────────────────────────────

    def _build_inventory_table(self, parent):
        hdr = tk.Frame(parent, bg="#1e1e2e")
        hdr.pack(fill="x", pady=(0, 4))
        tk.Label(hdr, text="Inventory", font=("Segoe UI", 13, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        tk.Button(hdr, text="⟳ Refresh", command=self._refresh_table,
                  **self._btn_style("#89dceb", small=True)).pack(side="right")

        cols = ("SKU", "Name", "Qty", "Unit Cost", "Total Value", "Last Updated")
        self.inv_tree = self._make_tree(parent, cols, height=10)

    # ─── Transaction Table ────────────────────────────────────────────────────

    def _build_transaction_table(self, parent):
        tk.Label(parent, text="Recent Transactions", font=("Segoe UI", 13, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", pady=(10, 4))

        cols = ("Timestamp", "Type", "SKU", "Delta", "Before", "After", "Value", "By")
        self.txn_tree = self._make_tree(parent, cols, height=7)

    # ─── Actions ──────────────────────────────────────────────────────────────

    def _add_item(self):
        sku  = getattr(self, "e_sku").get().strip()
        name = getattr(self, "e_name").get().strip()
        cost = getattr(self, "e_cost").get().strip()
        qty  = getattr(self, "e_qty").get().strip() or "0"
        desc = getattr(self, "e_desc").get().strip() or None
        by   = getattr(self, "e_created_by").get().strip() or None

        if not sku or not name:
            messagebox.showerror("Validation", "SKU and Name are required.")
            return
        try:
            cost = float(cost)
            qty  = int(qty)
        except ValueError:
            messagebox.showerror("Validation", "Unit Cost must be a number, Qty must be an integer.")
            return

        item, err = self.inv.create_item(sku=sku, name=name, unit_cost=cost,
                                         initial_quantity=qty, description=desc, created_by=by)
        if item:
            messagebox.showinfo("Success", f"Item '{item.name}' added successfully.")
            self._clear_fields("e_sku", "e_name", "e_cost", "e_qty", "e_desc", "e_created_by")
            self._refresh_table()
        else:
            messagebox.showerror("Error", err)

    def _stock_in(self):
        self._do_stock("in")

    def _stock_out(self):
        self._do_stock("out")

    def _do_stock(self, direction):
        sku   = getattr(self, "s_sku").get().strip()
        qty   = getattr(self, "s_qty").get().strip()
        ref   = getattr(self, "s_ref").get().strip() or None
        by    = getattr(self, "s_by").get().strip() or None
        notes = getattr(self, "s_notes").get().strip() or None

        if not sku:
            messagebox.showerror("Validation", "SKU is required.")
            return
        try:
            qty = int(qty)
        except ValueError:
            messagebox.showerror("Validation", "Quantity must be an integer.")
            return

        item = self.inv.get_by_sku(sku)
        if not item:
            messagebox.showerror("Error", f"Item with SKU '{sku}' not found.")
            return

        if direction == "in":
            result = self.txn.stock_in(item.id, qty, ref, by, notes)
        else:
            result = self.txn.stock_out(item.id, qty, ref, by, notes)

        if result.success:
            label = "Stock In" if direction == "in" else "Stock Out"
            messagebox.showinfo("Success", f"{label} of {qty} units recorded.")
            self._clear_fields("s_sku", "s_qty", "s_ref", "s_by", "s_notes")
            self._refresh_table()
        else:
            messagebox.showerror("Error", result.error)

    def _adjust(self):
        sku   = getattr(self, "a_sku").get().strip()
        qty   = getattr(self, "a_qty").get().strip()
        by    = getattr(self, "a_by").get().strip() or None
        notes = getattr(self, "a_notes").get().strip() or None

        if not sku:
            messagebox.showerror("Validation", "SKU is required.")
            return
        try:
            qty = int(qty)
        except ValueError:
            messagebox.showerror("Validation", "Quantity must be an integer.")
            return

        item = self.inv.get_by_sku(sku)
        if not item:
            messagebox.showerror("Error", f"Item with SKU '{sku}' not found.")
            return

        result = self.txn.adjust(item.id, qty, by, notes)
        if result.success:
            messagebox.showinfo("Success", f"Inventory adjusted to {qty} units.")
            self._clear_fields("a_sku", "a_qty", "a_by", "a_notes")
            self._refresh_table()
        else:
            messagebox.showerror("Error", result.error)

    # ─── Table Refresh ────────────────────────────────────────────────────────

    def _refresh_table(self):
        # Inventory
        for row in self.inv_tree.get_children():
            self.inv_tree.delete(row)

        items = self.inv.get_all_items()
        for item in sorted(items, key=lambda x: x.sku):
            total = item.quantity * item.unit_cost
            tag = "low" if item.quantity <= 5 else ""
            self.inv_tree.insert("", "end", values=(
                item.sku,
                item.name,
                item.quantity,
                f"${item.unit_cost:.2f}",
                f"${total:.2f}",
                item.last_updated.strftime("%Y-%m-%d %H:%M"),
            ), tags=(tag,))

        self.inv_tree.tag_configure("low", foreground="#f38ba8")

        # Transactions
        for row in self.txn_tree.get_children():
            self.txn_tree.delete(row)

        all_txns = self.sl.transaction_repo.get_all()
        for t in sorted(all_txns, key=lambda x: x.timestamp, reverse=True)[:50]:
            self.txn_tree.insert("", "end", values=(
                t.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                t.type.value,
                t.item_sku,
                f"{t.quantity_delta:+}",
                t.quantity_before,
                t.quantity_after,
                f"${t.total_value:.2f}",
                t.performed_by or "—",
            ))

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _card(self, parent, title):
        outer = tk.Frame(parent, bg="#313244", bd=0, pady=10, padx=12)
        outer.pack(fill="x", pady=(0, 10))
        tk.Label(outer, text=title, font=("Segoe UI", 11, "bold"),
                 bg="#313244", fg="#cdd6f4").pack(anchor="w", pady=(0, 6))
        return outer

    def _lbl_entry(self, parent, label, attr_name):
        tk.Label(parent, text=label, font=("Segoe UI", 9),
                 bg="#313244", fg="#a6adc8").pack(anchor="w")
        e = tk.Entry(parent, font=("Segoe UI", 10), bg="#45475a", fg="#cdd6f4",
                     insertbackground="#cdd6f4", relief="flat", bd=4)
        e.pack(fill="x", pady=(0, 4))
        setattr(self, attr_name, e)

    def _make_tree(self, parent, cols, height=8):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background="#313244", foreground="#cdd6f4",
                        rowheight=26, fieldbackground="#313244",
                        borderwidth=0, font=("Segoe UI", 9))
        style.configure("Custom.Treeview.Heading",
                        background="#45475a", foreground="#cdd6f4",
                        font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Custom.Treeview", background=[("selected", "#585b70")])

        frame = tk.Frame(parent, bg="#1e1e2e")
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            height=height, style="Custom.Treeview")

        col_widths = {"SKU": 90, "Name": 160, "Qty": 55, "Unit Cost": 80,
                      "Total Value": 90, "Last Updated": 130, "Timestamp": 140,
                      "Type": 90, "Delta": 55, "Before": 60, "After": 60,
                      "Value": 75, "By": 80}

        for col in cols:
            w = col_widths.get(col, 80)
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center" if col not in ("Name",) else "w")

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        return tree

    def _btn_style(self, bg, small=False):
        return dict(bg=bg, fg="#1e1e2e", font=("Segoe UI", 9 if small else 10, "bold"),
                    relief="flat", cursor="hand2", padx=8, pady=4 if small else 6)

    def _clear_fields(self, *attrs):
        for a in attrs:
            getattr(self, a).delete(0, tk.END)


if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
