import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { HelpCircle, X, Search } from "lucide-react";
import React, { useState, useEffect, useRef } from "react";

const helpQuestions = [
  {
    id: 1,
    category: "图片",
    question: "如何更换图片？",
    answer:
      "点击任意图片以显示图片工具栏。您将看到编辑、调整位置以及更改图片显示方式的选项。编辑选项允许您替换或修改当前图片。",
  },
  {
    id: 2,
    category: "图片",
    question: "可以使用AI生成新图片吗？",
    answer:
      "可以！点击任意图片并从工具栏中选择编辑。在显示的侧面板中，您将找到AI生成选项卡。输入描述您想要图片的提示词，我们的AI将根据您的描述生成图片。",
  },
  {
    id: 3,
    category: "图片",
    question: "如何上传自己的图片？",
    answer:
      "点击任意图片，然后从工具栏中选择编辑。在侧面板中，点击顶部的上传选项卡。您可以浏览文件以选择一个。上传后，您可以将其应用到您的设计中。",
  },
  {
    id: 11,
    category: "AI提示词",
    question: "可以通过提示词更改幻灯片布局吗？",
    answer:
      "可以！点击每张幻灯片左上角的魔棒图标，它会显示一个提示词输入框。描述您的布局要求，AI将相应地更改幻灯片布局。",
  },
  {
    id: 12,
    category: "AI提示词",
    question: "可以通过提示词更改幻灯片图片吗？",
    answer:
      "可以！点击每张幻灯片左上角的魔棒图标，它会显示一个提示词输入框。描述您想要的图片，AI将根据您的要求更新幻灯片图片。",
  },

  {
    id: 14,
    category: "AI提示词",
    question: "可以通过提示词更改内容吗？",
    answer:
      "可以！点击每张幻灯片左上角的魔棒图标，它会显示一个提示词输入框。描述您想要的内容，AI将根据您的描述更新幻灯片的文字和内容。",
  },
  {
    id: 4,
    category: "文字",
    question: "如何格式化和高亮文字？",
    answer:
      "选择任意文字以显示格式工具栏。您将获得加粗、斜体、下划线、删除线等选项。",
  },
  {
    id: 5,
    category: "图标",
    question: "如何更换图标？",
    answer:
      "点击任何现有图标进行修改。在图标选择面板中，您可以浏览图标或使用搜索功能查找特定图标。我们提供各种样式的数千个图标。",
  },
  {
    id: 16,
    category: "布局",
    question: "可以更改幻灯片的位置吗？",
    answer:
      "当然可以，在侧面板中您可以拖动幻灯片并将其放置到任何您想要的位置。",
  },
  {
    id: 15,
    category: "布局",
    question: "可以在幻灯片之间添加新幻灯片吗？",
    answer:
      "可以，只需点击每张幻灯片下方的加号图标。它将显示所有布局，您可以选择所需的布局。",
  },
  {
    id: 6,
    category: "布局",
    question: "可以向幻灯片添加更多部分吗？",
    answer:
      "当然可以！将鼠标悬停在任何文本框或内容块的底部，您将看到一个+图标出现。点击此按钮在当前部分下方添加新部分。您也可以使用插入菜单添加特定的部分类型。",
  },

  {
    id: 8,
    category: "导出",
    question: "如何下载或导出演示文稿？",
    answer:
      "点击右上角菜单中的导出按钮。您可以选择下载为PDF或PowerPoint格式。",
  },
];

const Help = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredQuestions, setFilteredQuestions] = useState(helpQuestions);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const modalRef = useRef<HTMLDivElement>(null);

  // Extract unique categories and create "All" category list
  useEffect(() => {
    const uniqueCategories = Array.from(
      new Set(helpQuestions.map((q) => q.category))
    );
    setCategories(["All", ...uniqueCategories]);
  }, []);

  // Filter questions based on search query and selected category
  useEffect(() => {
    let results = helpQuestions;

    // Filter by category if not "All"
    if (selectedCategory !== "All") {
      results = results.filter((q) => q.category === selectedCategory);
    }

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      results = results.filter(
        (q) =>
          q.question.toLowerCase().includes(query) ||
          q.answer.toLowerCase().includes(query)
      );
    }

    setFilteredQuestions(results);
  }, [searchQuery, selectedCategory]);

  // Close modal when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: any) => {
      if (
        modalRef.current &&
        !modalRef.current.contains(event.target) &&
        !event.target.closest(".help-button")
      ) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  const handleOpenClose = () => {
    setIsOpen(!isOpen);
  };

  // Animation helpers
  const modalClass = isOpen
    ? "opacity-100 scale-100"
    : "opacity-0 scale-95 pointer-events-none";

  return (
    <>
      {/* Help Button */}
      <button
        onClick={handleOpenClose}
        className="help-button hidden fixed bottom-6 right-6 h-12 w-12 z-50 bg-emerald-600 hover:bg-emerald-700 rounded-full md:flex justify-center items-center cursor-pointer shadow-lg transition-all duration-300 hover:shadow-xl"
        aria-label="Help Center"
      >
        {isOpen ? (
          <X className="text-white h-5 w-5" />
        ) : (
          <HelpCircle className="text-white h-5 w-5" />
        )}
      </button>

      {/* Help Modal */}
      <div
        className={`fixed bottom-20 right-6 z-50 max-w-md w-full transition-all duration-300 transform ${modalClass}`}
        ref={modalRef}
      >
        <div className="bg-white rounded-lg shadow-2xl border border-gray-200 overflow-hidden">
          {/* Header */}
          <div className="bg-emerald-600 text-white px-6 py-4 flex justify-between items-center">
            <h2 className="text-lg font-medium">帮助中心</h2>
            <button
              onClick={() => setIsOpen(false)}
              className="hover:bg-emerald-700 p-1 rounded"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Search */}
          <div className="px-6 pt-4 pb-2">
            <div className="relative">
              <input
                type="text"
                placeholder="搜索帮助主题..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
            </div>
          </div>

          {/* Category Pills */}
          <div className="px-6 pb-3 flex gap-2 overflow-x-auto hide-scrollbar">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-3 py-1 rounded-full text-sm whitespace-nowrap ${selectedCategory === category
                    ? "bg-emerald-600 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
              >
                {category}
              </button>
            ))}
          </div>

          {/* FAQ Accordion */}
          <div className="max-h-96 overflow-y-auto px-6 pb-6">
            {filteredQuestions.length > 0 ? (
              <Accordion type="single" collapsible className="w-full">
                {filteredQuestions.map((faq, index) => (
                  <AccordionItem
                    key={index}
                    value={`item-${index}`}
                    className="border-b border-gray-200 last:border-b-0"
                  >
                    <AccordionTrigger className="hover:no-underline py-3 px-1 text-left flex">
                      <div className="flex-1 pr-2">
                        <span className="text-gray-900 font-medium text-sm md:text-base">
                          {faq.question}
                        </span>
                        <span className="block text-xs text-emerald-600 mt-0.5">
                          {faq.category}
                        </span>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent className="px-1 pb-3">
                      <div className="text-sm text-gray-600 leading-relaxed rounded bg-gray-50 p-3">
                        {faq.answer}
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            ) : (
              <div className="py-8 text-center text-gray-500">
                <p>未找到"{searchQuery}"的相关结果</p>
                <button
                  onClick={() => {
                    setSearchQuery("");
                    setSelectedCategory("All");
                  }}
                  className="mt-2 text-emerald-600 hover:underline text-sm"
                >
                  清除搜索
                </button>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-3 border-t border-gray-200 text-xs text-gray-500 text-center">
            仍然需要帮助？{" "}
            <a href="/contact" className="text-emerald-600 hover:underline">
              联系支持
            </a>
          </div>
        </div>
      </div>

      {/* Custom AccordionTrigger implementation (since shadcn's might not be available) */}
      {!AccordionTrigger && (
        <style jsx>{`
          .accordion-trigger {
            display: flex;
            width: 100%;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 0;
            text-align: left;
            transition: all 0.2s;
          }
          .accordion-trigger:hover {
            background-color: rgba(0, 0, 0, 0.02);
          }
          .accordion-content {
            overflow: hidden;
            height: 0;
            transition: height 0.2s ease;
          }
          .accordion-content[data-state="open"] {
            height: auto;
          }
        `}</style>
      )}
    </>
  );
};

export default Help;
