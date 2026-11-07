
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


class FilePathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Path Scanner")
        self.root.geometry("950x650")
        self.root.minsize(700, 450)

        self.folder_var = tk.StringVar()
        self.extension_var = tk.StringVar(value="*")

        # Checkbox: Bao gồm tên thư mục gốc
        self.include_root_var = tk.BooleanVar(value=True)

        self.status_var = tk.StringVar(value="Sẵn sàng")
        self.paths = []

        main = ttk.Frame(root, padding=15)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="QUÉT DANH SÁCH ĐƯỜNG DẪN FILE",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(0, 15))

        # Nhập thư mục
        ttk.Label(
            main,
            text="Đường dẫn thư mục:"
        ).pack(anchor="w")

        folder_frame = ttk.Frame(main)
        folder_frame.pack(fill="x", pady=(5, 12))

        ttk.Entry(
            folder_frame,
            textvariable=self.folder_var
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            folder_frame,
            text="Chọn thư mục",
            command=self.choose_folder
        ).pack(side="left", padx=(8, 0))

        # Bộ lọc file
        filter_frame = ttk.Frame(main)
        filter_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(
            filter_frame,
            text="Lọc phần mở rộng:"
        ).pack(side="left")

        ttk.Entry(
            filter_frame,
            textvariable=self.extension_var,
            width=20
        ).pack(side="left", padx=8)

        ttk.Label(
            filter_frame,
            text="Ví dụ: * hoặc .spr hoặc .spr,.png"
        ).pack(side="left")

        # CHECKBOX MỚI
        options_frame = ttk.LabelFrame(
            main,
            text="Tùy chọn đường dẫn",
            padding=10
        )
        options_frame.pack(fill="x", pady=(0, 12))

        ttk.Checkbutton(
            options_frame,
            text="Bao gồm tên thư mục gốc trong đường dẫn",
            variable=self.include_root_var
        ).pack(anchor="w")

        ttk.Label(
            options_frame,
            text=(
                "Bật:   \\image\\hinh1\\bau.spr\n"
                "Tắt:   \\hinh1\\bau.spr"
            ),
            foreground="gray"
        ).pack(anchor="w", padx=22, pady=(5, 0))

        # Các nút
        button_frame = ttk.Frame(main)
        button_frame.pack(fill="x", pady=(0, 12))

        ttk.Button(
            button_frame,
            text="Quét file",
            command=self.scan_files
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            button_frame,
            text="Xuất TXT",
            command=self.export_txt
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            button_frame,
            text="Sao chép",
            command=self.copy_paths
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            button_frame,
            text="Xóa danh sách",
            command=self.clear_results
        ).pack(side="left")

        # Khu vực kết quả
        result_frame = ttk.Frame(main)
        result_frame.pack(fill="both", expand=True)

        self.text = tk.Text(
            result_frame,
            wrap="none",
            font=("Consolas", 10)
        )

        scroll_y = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.text.yview
        )

        scroll_x = ttk.Scrollbar(
            result_frame,
            orient="horizontal",
            command=self.text.xview
        )

        self.text.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        self.text.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        ttk.Label(
            main,
            textvariable=self.status_var
        ).pack(anchor="w", pady=(10, 0))

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def scan_files(self):
        folder = self.folder_var.get().strip().strip('"')

        if not folder:
            messagebox.showwarning(
                "Thiếu đường dẫn",
                "Vui lòng nhập hoặc chọn thư mục."
            )
            return

        root_path = Path(folder)

        if not root_path.is_dir():
            messagebox.showerror(
                "Lỗi",
                "Thư mục không tồn tại."
            )
            return

        # Lọc phần mở rộng
        filter_text = self.extension_var.get().strip()
        extensions = set()

        if filter_text and filter_text != "*":
            for ext in filter_text.split(","):
                ext = ext.strip().lower()

                if not ext:
                    continue

                if not ext.startswith("."):
                    ext = "." + ext

                extensions.add(ext)

        self.paths.clear()
        self.text.delete("1.0", tk.END)

        self.status_var.set("Đang quét file...")
        self.root.update_idletasks()

        try:
            files = (
                p for p in root_path.rglob("*")
                if p.is_file()
                and (
                    not extensions
                    or p.suffix.lower() in extensions
                )
            )

            for file in files:
                # Đường dẫn tương đối
                relative = file.relative_to(root_path)

                # Nếu checkbox được bật:
                # Thêm tên thư mục gốc vào đầu đường dẫn
                if self.include_root_var.get():
                    relative = Path(root_path.name) / relative

                # Chuyển sang đường dẫn Windows
                formatted = "\\" + str(relative).replace("/", "\\")

                self.paths.append(formatted)

            self.paths.sort(key=str.casefold)

            # Hiển thị kết quả
            self.text.insert(
                tk.END,
                "\n".join(self.paths)
            )

            self.status_var.set(
                f"Hoàn thành: {len(self.paths):,} file"
            )

        except Exception as e:
            messagebox.showerror(
                "Lỗi quét file",
                str(e)
            )

    def export_txt(self):
        if not self.paths:
            messagebox.showwarning(
                "Thông báo",
                "Chưa có danh sách file."
            )
            return

        output = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialfile="file_list.txt"
        )

        if not output:
            return

        try:
            with open(
                output,
                "w",
                encoding="utf-8-sig"
            ) as f:
                f.write("\n".join(self.paths) + "\n")

            messagebox.showinfo(
                "Thành công",
                f"Đã xuất {len(self.paths):,} đường dẫn."
            )

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def copy_paths(self):
        if not self.paths:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(
            "\n".join(self.paths)
        )

        self.status_var.set(
            f"Đã sao chép {len(self.paths):,} đường dẫn"
        )

    def clear_results(self):
        self.paths.clear()
        self.text.delete("1.0", tk.END)
        self.status_var.set("Đã xóa danh sách")


if __name__ == "__main__":
    root = tk.Tk()
    app = FilePathApp(root)
    root.mainloop()
