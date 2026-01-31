"use client";
import { useState, useEffect } from "react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./ui/tabs";
import { Check, ChevronsUpDown, Info } from "lucide-react";
import { Button } from "./ui/button";
import { Switch } from "./ui/switch";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "./ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
import { cn } from "@/lib/utils";
import OpenAIConfig from "./OpenAIConfig";
import GoogleConfig from "./GoogleConfig";
import AnthropicConfig from "./AnthropicConfig";
import OllamaConfig from "./OllamaConfig";
import CustomConfig from "./CustomConfig";
import {
  updateLLMConfig,
  changeProvider as changeProviderUtil,
} from "@/utils/providerUtils";
import { IMAGE_PROVIDERS, LLM_PROVIDERS } from "@/utils/providerConstants";
import { LLMConfig } from "@/types/llm_config";

const DALLE_3_QUALITY_OPTIONS = [
  {
    label: "标准",
    value: "standard",
    description: "更快的生成速度，更低的成本",
  },
  {
    label: "高清",
    value: "hd",
    description: "更高质量的图片，但成本更高",
  },
];

const GPT_IMAGE_1_5_QUALITY_OPTIONS = [
  {
    label: "低",
    value: "low",
    description: "最快且最具成本效益",
  },
  {
    label: "中",
    value: "medium",
    description: "平衡的质量和速度",
  },
  {
    label: "高",
    value: "high",
    description: "最佳质量，生成时间较长",
  },
];

// Button state interface
interface ButtonState {
  isLoading: boolean;
  isDisabled: boolean;
  text: string;
  showProgress: boolean;
  progressPercentage?: number;
  status?: string;
}

interface LLMProviderSelectionProps {
  initialLLMConfig: LLMConfig;
  onConfigChange: (config: LLMConfig) => void;
  buttonState: ButtonState;
  setButtonState: (
    state: ButtonState | ((prev: ButtonState) => ButtonState)
  ) => void;
}

export default function LLMProviderSelection({
  initialLLMConfig,
  onConfigChange,
  setButtonState,
}: LLMProviderSelectionProps) {
  const [llmConfig, setLlmConfig] = useState<LLMConfig>(initialLLMConfig);
  const [openImageProviderSelect, setOpenImageProviderSelect] = useState(false);
  const isImageGenerationDisabled = llmConfig.DISABLE_IMAGE_GENERATION ?? false;

  useEffect(() => {
    onConfigChange(llmConfig);
  }, [llmConfig]);

  useEffect(() => {
    const needsModelSelection =
      (llmConfig.LLM === "openai" && !llmConfig.OPENAI_MODEL) ||
      (llmConfig.LLM === "google" && !llmConfig.GOOGLE_MODEL) ||
      (llmConfig.LLM === "ollama" && !llmConfig.OLLAMA_MODEL) ||
      (llmConfig.LLM === "custom" && !llmConfig.CUSTOM_MODEL) ||
      (llmConfig.LLM === "anthropic" && !llmConfig.ANTHROPIC_MODEL);

    const needsProviderApiKey =
      (llmConfig.LLM === "openai" && !llmConfig.OPENAI_API_KEY) ||
      (llmConfig.LLM === "google" && !llmConfig.GOOGLE_API_KEY) ||
      (llmConfig.LLM === "anthropic" && !llmConfig.ANTHROPIC_API_KEY);

    const needsImageProviderApiKey =
      !llmConfig.DISABLE_IMAGE_GENERATION &&
      ((llmConfig.IMAGE_PROVIDER === "dall-e-3" && !llmConfig.OPENAI_API_KEY) ||
        (llmConfig.IMAGE_PROVIDER === "gpt-image-1.5" &&
          !llmConfig.OPENAI_API_KEY) ||
        (llmConfig.IMAGE_PROVIDER === "gemini_flash" &&
          !llmConfig.GOOGLE_API_KEY) ||
        (llmConfig.IMAGE_PROVIDER === "nanobanana_pro" &&
          !llmConfig.GOOGLE_API_KEY) ||
        (llmConfig.IMAGE_PROVIDER === "pexels" && !llmConfig.PEXELS_API_KEY) ||
        (llmConfig.IMAGE_PROVIDER === "pixabay" && !llmConfig.PIXABAY_API_KEY));

    const needsApiKey = needsProviderApiKey || needsImageProviderApiKey;

    const needsOllamaUrl = llmConfig.LLM === "ollama" && !llmConfig.OLLAMA_URL;

    const needsComfyUIConfig =
      !llmConfig.DISABLE_IMAGE_GENERATION &&
      llmConfig.IMAGE_PROVIDER === "comfyui" &&
      (!llmConfig.COMFYUI_URL || !llmConfig.COMFYUI_WORKFLOW);

    setButtonState({
      isLoading: false,
      isDisabled:
        needsModelSelection ||
        needsApiKey ||
        needsOllamaUrl ||
        needsComfyUIConfig,
      text: needsModelSelection
        ? "请选择模型"
        : needsApiKey
        ? "请输入API密钥"
        : needsOllamaUrl
        ? "请输入Ollama URL"
        : needsComfyUIConfig
        ? "请配置ComfyUI"
        : "保存配置",
      showProgress: false,
    });
  }, [llmConfig]);

  const input_field_changed = (new_value: string | boolean, field: string) => {
    const updatedConfig = updateLLMConfig(llmConfig, field, new_value);
    setLlmConfig(updatedConfig);
  };

  const getApiKeyValue = (field?: string) => {
    switch (field) {
      case "OPENAI_API_KEY":
        return llmConfig.OPENAI_API_KEY || "";
      case "GOOGLE_API_KEY":
        return llmConfig.GOOGLE_API_KEY || "";
      case "ANTHROPIC_API_KEY":
        return llmConfig.ANTHROPIC_API_KEY || "";
      case "PEXELS_API_KEY":
        return llmConfig.PEXELS_API_KEY || "";
      case "PIXABAY_API_KEY":
        return llmConfig.PIXABAY_API_KEY || "";
      default:
        return "";
    }
  };

  const handleApiKeyInputChange = (field: string | undefined, value: string) => {
    switch (field) {
      case "OPENAI_API_KEY":
        input_field_changed(value, "openai_api_key");
        break;
      case "GOOGLE_API_KEY":
        input_field_changed(value, "google_api_key");
        break;
      case "ANTHROPIC_API_KEY":
        input_field_changed(value, "anthropic_api_key");
        break;
      case "PEXELS_API_KEY":
        input_field_changed(value, "pexels_api_key");
        break;
      case "PIXABAY_API_KEY":
        input_field_changed(value, "pixabay_api_key");
        break;
      default:
        break;
    }
  };

  const handleProviderChange = (provider: string) => {
    const newConfig = changeProviderUtil(llmConfig, provider);
    setLlmConfig(newConfig);
  };

  useEffect(() => {
    if (!llmConfig.USE_CUSTOM_URL) {
      setLlmConfig({ ...llmConfig, OLLAMA_URL: "http://localhost:11434" });
    } else {
      if (!llmConfig.OLLAMA_URL) {
        setLlmConfig({ ...llmConfig, OLLAMA_URL: "http://localhost:11434" });
      }
    }
  }, [llmConfig.USE_CUSTOM_URL]);

  useEffect(() => {
    setLlmConfig((prevConfig) => {
      const updates: Partial<LLMConfig> = {};

      if (!prevConfig.DISABLE_IMAGE_GENERATION && !prevConfig.IMAGE_PROVIDER) {
        if (prevConfig.LLM === "openai") {
          updates.IMAGE_PROVIDER = "gpt-image-1.5";
        } else if (prevConfig.LLM === "google") {
          updates.IMAGE_PROVIDER = "gemini_flash";
        } else {
          updates.IMAGE_PROVIDER = "pexels";
        }
      }

      if (!prevConfig.OLLAMA_URL) {
        updates.OLLAMA_URL = "http://localhost:11434";
      }

      if (Object.keys(updates).length === 0) {
        return prevConfig;
      }

      return { ...prevConfig, ...updates };
    });
  }, []);

  useEffect(() => {
    setLlmConfig((prevConfig) => {
      const updates: Partial<LLMConfig> = {};

      if (
        prevConfig.IMAGE_PROVIDER === "dall-e-3" &&
        !prevConfig.DALL_E_3_QUALITY
      ) {
        updates.DALL_E_3_QUALITY = "standard";
      }

      if (
        prevConfig.IMAGE_PROVIDER === "gpt-image-1.5" &&
        !prevConfig.GPT_IMAGE_1_5_QUALITY
      ) {
        updates.GPT_IMAGE_1_5_QUALITY = "medium";
      }

      if (Object.keys(updates).length === 0) {
        return prevConfig;
      }

      return { ...prevConfig, ...updates };
    });
  }, [llmConfig.IMAGE_PROVIDER]);

  const renderQualitySelector = () => {
    if (llmConfig.IMAGE_PROVIDER === "dall-e-3") {
      return (
        <div className="mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            DALL·E 3 图片质量
          </label>
          <div className="grid grid-cols-2 gap-3">
            {DALLE_3_QUALITY_OPTIONS.map((option) => (
              <button
                key={option.value}
                type="button"
                className={cn(
                  "border rounded-lg p-3 text-left transition-colors",
                  llmConfig.DALL_E_3_QUALITY === option.value
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200 hover:border-gray-300"
                )}
                onClick={() =>
                  input_field_changed(option.value, "dall_e_3_quality")
                }
              >
                <div className="text-sm font-medium text-gray-900">
                  {option.label}
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {option.description}
                </div>
              </button>
            ))}
          </div>
        </div>
      );
    }

    if (llmConfig.IMAGE_PROVIDER === "gpt-image-1.5") {
      return (
        <div className="mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            GPT Image 1.5 质量
          </label>
          <div className="grid grid-cols-3 gap-3">
            {GPT_IMAGE_1_5_QUALITY_OPTIONS.map((option) => (
              <button
                key={option.value}
                type="button"
                className={cn(
                  "border rounded-lg p-3 text-left transition-colors",
                  llmConfig.GPT_IMAGE_1_5_QUALITY === option.value
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200 hover:border-gray-300"
                )}
                onClick={() =>
                  input_field_changed(option.value, "gpt_image_1_5_quality")
                }
              >
                <div className="text-sm font-medium text-gray-900">
                  {option.label}
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {option.description}
                </div>
              </button>
            ))}
          </div>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="h-full flex flex-col mt-10">
      {/* Provider Selection - Fixed Header */}
      <div className="p-2 rounded-2xl border border-gray-200">
        <Tabs
          value={llmConfig.LLM || "openai"}
          onValueChange={handleProviderChange}
          className="w-full"
        >
          <TabsList className="grid w-full grid-cols-5 bg-transparent h-10">
            <TabsTrigger value="openai">OpenAI</TabsTrigger>
            <TabsTrigger value="google">Google</TabsTrigger>
            <TabsTrigger value="anthropic">Anthropic</TabsTrigger>
            <TabsTrigger value="ollama">Ollama</TabsTrigger>
            <TabsTrigger value="custom">Custom</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto p-6 pt-0 custom_scrollbar">
        <Tabs
          value={llmConfig.LLM || "openai"}
          onValueChange={handleProviderChange}
          className="w-full"
        >
          {/* OpenAI Content */}
          <TabsContent value="openai" className="mt-6">
            <OpenAIConfig
              openaiApiKey={llmConfig.OPENAI_API_KEY || ""}
              openaiModel={llmConfig.OPENAI_MODEL || ""}
              webGrounding={llmConfig.WEB_GROUNDING || false}
              onInputChange={input_field_changed}
            />
          </TabsContent>

          {/* Google Content */}
          <TabsContent value="google" className="mt-6">
            <GoogleConfig
              googleApiKey={llmConfig.GOOGLE_API_KEY || ""}
              googleModel={llmConfig.GOOGLE_MODEL || ""}
              webGrounding={llmConfig.WEB_GROUNDING || false}
              onInputChange={input_field_changed}
            />
          </TabsContent>

          {/* Anthropic Content */}
          <TabsContent value="anthropic" className="mt-6">
            <AnthropicConfig
              anthropicApiKey={llmConfig.ANTHROPIC_API_KEY || ""}
              anthropicModel={llmConfig.ANTHROPIC_MODEL || ""}
              extendedReasoning={llmConfig.EXTENDED_REASONING || false}
              webGrounding={llmConfig.WEB_GROUNDING || false}
              onInputChange={input_field_changed}
            />
          </TabsContent>

          {/* Ollama Content */}
          <TabsContent value="ollama" className="mt-6">
            <OllamaConfig
              ollamaModel={llmConfig.OLLAMA_MODEL || ""}
              ollamaUrl={llmConfig.OLLAMA_URL || ""}
              useCustomUrl={llmConfig.USE_CUSTOM_URL || false}
              onInputChange={input_field_changed}
            />
          </TabsContent>

          {/* Custom Content */}
          <TabsContent value="custom" className="mt-6">
            <CustomConfig
              customLlmUrl={llmConfig.CUSTOM_LLM_URL || ""}
              customLlmApiKey={llmConfig.CUSTOM_LLM_API_KEY || ""}
              customModel={llmConfig.CUSTOM_MODEL || ""}
              toolCalls={llmConfig.TOOL_CALLS || false}
              disableThinking={llmConfig.DISABLE_THINKING || false}
              onInputChange={input_field_changed}
            />
          </TabsContent>
        </Tabs>

        {/* Image Generation Toggle */}
        <div className="my-8">
          <div className="flex items-center justify-between mb-4 bg-green-50 p-2 rounded-sm">
            <label className="text-sm font-medium text-gray-700">
              禁用图片生成
            </label>
            <Switch
              checked={isImageGenerationDisabled}
              onCheckedChange={(checked) => {
                input_field_changed(checked, "disable_image_generation");
                if (checked) {
                  setOpenImageProviderSelect(false);
                }
              }}
            />
          </div>
          <p className="text-sm text-gray-500 flex items-center gap-2">
            <span className="block w-1 h-1 rounded-full bg-gray-400"></span>
            启用后，幻灯片将不包含自动生成的图片。
          </p>
        </div>

        {!isImageGenerationDisabled && (
          <>
            {/* Image Provider Selection */}
            <div className="my-8">
              <label className="block text-sm font-medium text-gray-700 mb-3">
                选择图片提供商
              </label>
              <div className="w-full">
                <Popover
                  open={openImageProviderSelect}
                  onOpenChange={setOpenImageProviderSelect}
                >
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      role="combobox"
                      aria-expanded={openImageProviderSelect}
                      className="w-full h-12 px-4 py-4 outline-none border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors hover:border-gray-400 justify-between"
                    >
                      <div className="flex gap-3 items-center">
                        <span className="text-sm font-medium text-gray-900">
                          {llmConfig.IMAGE_PROVIDER
                            ? IMAGE_PROVIDERS[llmConfig.IMAGE_PROVIDER]
                                ?.label || llmConfig.IMAGE_PROVIDER
                            : "选择图片提供商"}
                        </span>
                      </div>
                      <ChevronsUpDown className="w-4 h-4 text-gray-500" />
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent
                    className="p-0"
                    align="start"
                    style={{ width: "var(--radix-popover-trigger-width)" }}
                  >
                    <Command>
                      <CommandInput placeholder="搜索提供商..." />
                      <CommandList>
                        <CommandEmpty>未找到提供商。</CommandEmpty>
                        <CommandGroup>
                          {Object.values(IMAGE_PROVIDERS).map(
                            (provider, index) => (
                              <CommandItem
                                key={index}
                                value={provider.value}
                                onSelect={(value) => {
                                  input_field_changed(value, "image_provider");
                                  setOpenImageProviderSelect(false);
                                }}
                              >
                                <Check
                                  className={cn(
                                    "mr-2 h-4 w-4",
                                    llmConfig.IMAGE_PROVIDER === provider.value
                                      ? "opacity-100"
                                      : "opacity-0"
                                  )}
                                />
                                <div className="flex gap-3 items-center">
                                  <div className="flex flex-col space-y-1 flex-1">
                                    <div className="flex items-center justify-between gap-2">
                                      <span className="text-sm font-medium text-gray-900 capitalize">
                                        {provider.label}
                                      </span>
                                    </div>
                                    <span className="text-xs text-gray-600 leading-relaxed">
                                      {provider.description}
                                    </span>
                                  </div>
                                </div>
                              </CommandItem>
                            )
                          )}
                        </CommandGroup>
                      </CommandList>
                    </Command>
                  </PopoverContent>
                </Popover>
              </div>
            </div>

            {renderQualitySelector()}

            {/* Dynamic API Key Input for Image Provider */}
            {llmConfig.IMAGE_PROVIDER &&
              IMAGE_PROVIDERS[llmConfig.IMAGE_PROVIDER] &&
              (() => {
                const provider = IMAGE_PROVIDERS[llmConfig.IMAGE_PROVIDER];

                // Show info message when using same API key as main provider
                if (
                  provider.value === "dall-e-3" &&
                  llmConfig.LLM === "openai"
                ) {
                  return <></>;
                }

                if (
                  provider.value === "gpt-image-1.5" &&
                  llmConfig.LLM === "openai"
                ) {
                  return <></>;
                }

                if (
                  provider.value === "gemini_flash" &&
                  llmConfig.LLM === "google"
                ) {
                  return <></>;
                }

                if (
                  provider.value === "nanobanana_pro" &&
                  llmConfig.LLM === "google"
                ) {
                  return <></>;
                }

                // Show ComfyUI configuration
                if (provider.value === "comfyui") {
                  return (
                    <div className="mb-8 space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          ComfyUI 服务器 URL
                        </label>
                        <div className="relative">
                          <input
                            type="text"
                            placeholder="http://192.168.1.7:8188"
                            className="w-full px-4 py-2.5 outline-none border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
                            value={llmConfig.COMFYUI_URL || ""}
                            onChange={(e) => {
                              input_field_changed(
                                e.target.value,
                                "comfyui_url"
                              );
                            }}
                          />
                        </div>
                        <p className="mt-2 text-sm text-gray-500 flex items-center gap-2">
                          <span className="block w-1 h-1 rounded-full bg-gray-400"></span>
                          在Docker中运行时，请使用机器的IP地址（而不是localhost）
                        </p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Workflow JSON
                        </label>
                        <div className="relative">
                          <textarea
                            placeholder='Paste your ComfyUI workflow JSON here (export via "Export (API)" in ComfyUI)'
                            className="w-full px-4 py-2.5 outline-none border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors font-mono text-xs"
                            rows={6}
                            value={llmConfig.COMFYUI_WORKFLOW || ""}
                            onChange={(e) => {
                              input_field_changed(
                                e.target.value,
                                "comfyui_workflow"
                              );
                            }}
                          />
                        </div>
                        <p className="mt-2 text-sm text-gray-500">
                          Export your workflow from ComfyUI using &quot;Export
                          (API)&quot; and paste the JSON here.
                        </p>
                      </div>
                    </div>
                  );
                }

                // Show API key input for other providers
                return (
                  <div className="mb-8">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {provider.apiKeyFieldLabel}
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        placeholder={`输入您的${provider.apiKeyFieldLabel}`}
                        className="w-full px-4 py-2.5 outline-none border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
                        value={getApiKeyValue(provider.apiKeyField)}
                        onChange={(e) =>
                          handleApiKeyInputChange(
                            provider.apiKeyField,
                            e.target.value
                          )
                        }
                      />
                    </div>
                    <p className="mt-2 text-sm text-gray-500 flex items-center gap-2">
                      <span className="block w-1 h-1 rounded-full bg-gray-400"></span>
                      {provider.label} 图片生成的API密钥
                    </p>
                  </div>
                );
              })()}
          </>
        )}

        {/* Model Information */}
        <div className="mb-8 p-4 bg-blue-50 rounded-lg border border-blue-100">
          <div className="flex items-start gap-3">
            <Info className="w-5 h-5 text-blue-500 mt-0.5" />
            <div>
              <h3 className="text-sm font-medium text-blue-900 mb-1">
                已选模型
              </h3>
              <p className="text-sm text-blue-700">
                使用{" "}
                {llmConfig.LLM === "ollama"
                  ? llmConfig.OLLAMA_MODEL ?? "xxxxx"
                  : llmConfig.LLM === "custom"
                  ? llmConfig.CUSTOM_MODEL ?? "xxxxx"
                  : llmConfig.LLM === "anthropic"
                  ? llmConfig.ANTHROPIC_MODEL ?? "xxxxx"
                  : llmConfig.LLM === "google"
                  ? llmConfig.GOOGLE_MODEL ?? "xxxxx"
                  : llmConfig.LLM === "openai"
                  ? llmConfig.OPENAI_MODEL ?? "xxxxx"
                  : "xxxxx"}{" "}
                进行文本生成{" "}
                {isImageGenerationDisabled ? (
                  "，图片生成已禁用。"
                ) : (
                  <>
                    和{" "}
                    {llmConfig.IMAGE_PROVIDER &&
                    IMAGE_PROVIDERS[llmConfig.IMAGE_PROVIDER]
                      ? IMAGE_PROVIDERS[llmConfig.IMAGE_PROVIDER].label
                      : "xxxxx"}{" "}
                    进行图片生成
                  </>
                )}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
