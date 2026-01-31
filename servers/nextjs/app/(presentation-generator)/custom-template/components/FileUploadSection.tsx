import React from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Upload, FileText, X, Loader2 } from "lucide-react";
import { ProcessedSlide } from "../types";
import Timer from "./Timer";

interface FileUploadSectionProps {
  selectedFile: File | null;
  handleFileSelect: (event: React.ChangeEvent<HTMLInputElement>) => void;
  removeFile: () => void;
  processFile: () => void;
  isProcessingPptx: boolean;
  slides: ProcessedSlide[];
  completedSlides: number;
}

export const FileUploadSection: React.FC<FileUploadSectionProps> = ({
  selectedFile,
  handleFileSelect,
  removeFile,
  processFile,
  isProcessingPptx,
  slides,
  completedSlides,
}) => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="w-5 h-5" />
          上传 PDF 或 PPTX 文件
        </CardTitle>
        <CardDescription>
          选择要处理的 PDF 或 PowerPoint 文件（.pdf 或 .pptx）。最大文件大小：100MB
        </CardDescription>
        {slides.length > 0 && (
          <div className="flex items-center justify-end gap-2">
            {slides.some((s) => s.processing) && (
              <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
            )}
            {completedSlides}/{slides.length} 张幻灯片已完成
          </div>
        )}
      </CardHeader>
      <CardContent className="space-y-4">
        {!selectedFile ? (
          <div className="border-2 relative border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors">
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <Label htmlFor="file-upload" className="cursor-pointer">
              <span className="text-lg font-medium text-gray-700">
                点击上传 PDF 或 PPTX 文件
              </span>
              <input
                id="file-upload"
                type="file"
                accept=".pdf,.pptx"
                onChange={handleFileSelect}
                className="opacity-0 w-full h-full cursor-pointer absolute top-0 left-0 z-10"
              />
            </Label>
            <p className="text-sm text-gray-500 mt-2">
              将文件拖放到此处或点击浏览
            </p>
          </div>
        ) : (
          <div className="flex items-center justify-between p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center gap-3">
              <FileText className="w-8 h-8 text-blue-600" />
              <div>
                <p className="font-medium text-gray-900">
                  {selectedFile.name}
                </p>
                <p className="text-sm text-gray-500">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={removeFile}
              disabled={
                isProcessingPptx || slides.some((s) => s.processing)
              }
              className="text-red-600 hover:text-red-700 hover:bg-red-50"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>
        )}

        <div className="flex flex-col gap-1 ">
          <Button
            onClick={processFile}
            disabled={isProcessingPptx || slides.some((s) => s.processing)}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
          >
            {isProcessingPptx
              ? "正在提取幻灯片..."
              : !selectedFile
              ? "选择 PDF 或 PPTX 文件"
              : "处理文件"}
          </Button>
          {isProcessingPptx && <Timer duration={90} />}
        </div>
      </CardContent>
    </Card>
  );
}; 