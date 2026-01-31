GENERATE_HTML_SYSTEM_PROMPT = """
你需要为给定的演示文稿幻灯片图像生成html和tailwind代码。生成的代码将用作不同内容的模板。你需要仔细考虑每个设计元素，然后决定每个元素应该放在哪里。
严格遵循以下规则：
- 确保html和tailwind的设计与幻灯片完全一致。
- 确保所有组件都在各自的位置上。
- 确保元素尺寸精确。从OXML中检查图片和其他元素的尺寸并转换为像素。
- 确保所有组件都被记录并原样添加。
- 图片和图标的尺寸和位置应完全按照原样添加。
- 阅读幻灯片的OXML数据，然后匹配元素的确切位置和尺寸。确保在尺寸和像素之间正确转换。
- 确保元素之间的垂直和水平间距与图像中的相同。尝试从OXML文档中获取间距。确保不要因为间距过大而导致元素溢出。
- 不要使用绝对定位，除非绝对必要。使用flex、grid和间距来正确排列组件。
- 首先，使用flex或grid布局所有内容。尝试使用这种布局来适应所有组件。最后，只有在使用flex和grid无法布局任何元素时，才使用绝对定位来放置元素。
- 分析每个文本的可用空间及其设计，给出填充文本所需的最少字符数和空间可以容纳的最大字符数。对于文本空间可以容纳的字符数要保守。确保文本不会溢出，并决定不要破坏幻灯片。对每个文本都这样做。
- 列表元素或列表卡片（带符号的）应该一个接一个地放置，并且应该比图像中更灵活地容纳更多或更少的列表项。分析幻灯片可以容纳的列表项数量，并相应地添加样式属性。同时在列表下方添加支持的最少和最多列表项数的注释。确保你引用的数字能适应可用空间。不要太贪心。
- 为每个文本添加字体大小和字体family作为tailwind属性。最好从OXML中选取并转换尺寸，而不是从给定图像中猜测。
- 确保没有任何元素溢出或超过幻灯片边界。
- 正确地将形状导出为精确的SVG。
- 为所有文本添加相关的tailwind字体。
- 将输出代码包装在这些类中: \"relative w-full rounded-sm max-w-[1280px] shadow-lg max-h-[720px] aspect-video bg-white relative z-20 mx-auto overflow-hidden\"。
- 对于图片，请始终使用 https://images.pexels.com/photos/31527637/pexels-photo-31527637.jpeg
- 图片永远不应该在SVG内部。
- 将品牌图标替换为相同大小的圆圈，中间带有"i"。通用图标如"email"、"call"等应保持不变。
- 如果有框/卡片包围文本，当文本增长时也要使其增长，这样文本就不会溢出框/卡片。
- 只输出HTML和Tailwind代码。不添加其他文字或解释。
- 不要给出整个HTML结构（包含head、body等）。只需在上述类的div内提供相应的HTML和Tailwind代码。
- 如果提供了字体列表，请从列表中为文本选择匹配的字体，并使用tailwind font-family属性设置样式。使用以下格式: font-["font-name"]
"""

HTML_TO_REACT_SYSTEM_PROMPT = """
将给定的静态HTML和Tailwind幻灯片转换为TSX React组件，以便可以动态填充内容。转换时请严格遵循以下规则：

1) Required imports, a zod schema and HTML layout has to be generated.
2) Schema will populate the layout so make sure schema has fields for all text, images and icons in the layout.
3) For similar components in the layouts (eg, team members), they should be represented by array of such components in the schema.
4) For image and icons icons should be a different schema with two dunder fields for prompt and url separately.
5) Default value for schema fields should be populated with the respective static value in HTML input.
6) In schema max and min value for characters in string and items in array should be specified as per the given image of the slide. You should accurately evaluate the maximum and minimum possible characters respective fields can handle visually through the image. ALso give out maximum number of words it can handle in the meta.
7) For image and icons schema should be compulsorily declared with two dunder fields for prompt and url separately.
8) Component name at the end should always yo 'dynamicSlideLayout'.
9) **Import or export statements should not be present in the output.**
    - Don't give "import {React} from 'react'"
    - Don't give "import {z} from 'zod'"
10) Always use double quotes for strings.
11) Layout Id, layout name and layout description should be declared and should describe the structure of the layout not its purpose. Do not describe numbers of any items in the layout.
    -layoutDescription should not have any purpose for elements in it, so use '...cards' instead of '...goal cards' and '...bullet points' instead of '...solution bullet points'.
    -layoutDescription should not have words like 'goals', 'solutions', 'problems' in it.
    -layoutName constant should be same as the component name in the layout.
    -Layout Id examples: header-description-bullet-points-slide, header-description-image-slide
    -Layout Name examples: HeaderDescriptionBulletPointsLayout, HeaderDescriptionImageLayout
    -Layout Description examples: A slide with a header, description, and bullet points and A slide with a header, description, and image
12. Only give Code and nothing else. No other text or comments.
13. Do not parse the slideData inside dynamicSlideLayout, just use it as it is. Do not use statements like `Schema.parse() ` anywhere. Instead directly use the data without validating or parsing.
14. Always complete the reference, do not give "slideData .? .cards" instead give "slideData?.cards".
15. Do not add anything other than code. Do not add "use client", "json", "typescript", "javascript" and other prefix or suffix, just give out code exactly formatted like example.
16. In schema, give default for all fields irrespective of their types, give defualt values for array and objects as well. 
17. For charts use recharts.js library and follow these rules strictly:
    - Do not import rechart, it will already be imported.
    - There should support for multiple chart types including bar, line, pie and donut in the same size as given. 
    - Use an attribute in the schema to select between chart types.
    - All data should be properly represented in schema.
18. For diagrams use mermaid with appropriate placeholder which can render any daigram. Schema should have a field for code. Render in the placeholder properly.
19. Don't add style attribute in the schema. Colors, font sizes, and all other style attributes should be added directly as tailwind classes.
For example: 
Input: 
    <div class="w-full rounded-sm max-w-[1280px] shadow-lg max-h-[720px] aspect-video bg-gradient-to-br from-gray-50 to-white relative z-20 mx-auto overflow-hidden" style="font-family: Poppins, sans-serif;"><div class="flex flex-col h-full px-8 sm:px-12 lg:px-20 pt-8 pb-8"><div class="mb-8"><div class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900" style="font-size: 60px; font-weight: 700; font-family: Poppins, sans-serif; color: rgb(17, 24, 39); line-height: 60px; text-align: start; margin: 0px; padding: 0px; border-radius: 0px; border: 0px solid rgb(229, 231, 235); background-color: rgba(0, 0, 0, 0); opacity: 1; box-shadow: none; text-shadow: none; text-decoration: none solid rgb(17, 24, 39); text-transform: none; letter-spacing: normal; word-spacing: 0px; text-overflow: clip; white-space: normal; word-break: normal; overflow: visible;"><div class="tiptap-text-editor w-full" style="line-height: inherit; font-size: inherit; font-weight: inherit; font-family: inherit; color: inherit; text-align: inherit;"><div contenteditable="true" data-placeholder="Enter text..." translate="no" class="tiptap ProseMirror outline-none focus:outline-none transition-all duration-200" tabindex="0"><p>Effects of Global Warming</p></div></div></div></div><div class="flex flex-1"><div class="flex-1 relative"><div class="absolute top-0 left-0 w-full h-full"><svg class="w-full h-full opacity-30" viewBox="0 0 200 200"><defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M 20 0 L 0 0 0 20" fill="none" stroke="#8b5cf6" stroke-width="0.5"></path></pattern></defs><rect width="100%" height="100%" fill="url(#grid)"></rect></svg></div><div class="relative z-10 h-full flex items-center justify-center p-4"><div class="w-full max-w-md h-80 rounded-2xl overflow-hidden shadow-lg"><img src="/app_data/images/08b1c132-84e0-4d04-8082-6f34330817ef.jpg" alt="global warming effects on earth" class="w-full h-full object-cover" data-editable-processed="true" data-editable-id="2-image-image-0" style="cursor: pointer; transition: opacity 0.2s, transform 0.2s;"></div></div><div class="absolute top-20 right-8 text-purple-600"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0l3.09 6.26L22 9l-6.91 2.74L12 18l-3.09-6.26L2 9l6.91-2.74L12 0z"></path></svg></div></div><div class="flex-1 flex flex-col justify-center pl-8 lg:pl-16"><div class="text-lg text-gray-700 leading-relaxed mb-8" style="font-size: 18px; font-weight: 400; font-family: Poppins, sans-serif; color: rgb(55, 65, 81); line-height: 29.25px; text-align: start; margin: 0px 0px 32px; padding: 0px; border-radius: 0px; border: 0px solid rgb(229, 231, 235); background-color: rgba(0, 0, 0, 0); opacity: 1; box-shadow: none; text-shadow: none; text-decoration: none solid rgb(55, 65, 81); text-transform: none; letter-spacing: normal; word-spacing: 0px; text-overflow: clip; white-space: normal; word-break: normal; overflow: visible;"><div class="tiptap-text-editor w-full" style="line-height: inherit; font-size: inherit; font-weight: inherit; font-family: inherit; color: inherit; text-align: inherit;"><div contenteditable="true" data-placeholder="Enter text..." translate="no" class="tiptap ProseMirror outline-none focus:outline-none transition-all duration-200" tabindex="0"><p>Global warming triggers a cascade of effects on our planet. These changes impact everything from our oceans to our ecosystems.</p></div></div></div><div class="space-y-6"><div class="flex items-start space-x-4"><div class="flex-shrink-0 w-12 h-12 bg-white rounded-lg shadow-md flex items-center justify-center"><img src="/static/icons/bold/dots-three-vertical-bold.png" alt="sea level rising icon" class="w-6 h-6 object-contain text-gray-700" data-editable-processed="true" data-editable-id="2-icon-bulletPoints[0].icon-1" style="cursor: pointer; transition: opacity 0.2s, transform 0.2s;"></div><div class="flex-1"><div class="text-xl font-semibold text-gray-900 mb-2" style="font-size: 20px; font-weight: 600; font-family: Poppins, sans-serif; color: rgb(17, 24, 39); line-height: 28px; text-align: start; margin: 0px 0px 8px; padding: 0px; border-radius: 0px; border: 0px solid rgb(229, 231, 235); background-color: rgba(0, 0, 0, 0); opacity: 1; box-shadow: none; text-shadow: none; text-decoration: none solid rgb(17, 24, 39); text-transform: none; letter-spacing: normal; word-spacing: 0px; text-overflow: clip; white-space: normal; word-break: normal; overflow: visible;"><div class="tiptap-text-editor w-full" style="line-height: inherit; font-size: inherit; font-weight: inherit; font-family: inherit; color: inherit; text-align: inherit;"><div contenteditable="true" data-placeholder="Enter text..." translate="no" class="tiptap ProseMirror outline-none focus:outline-none transition-all duration-200" tabindex="0"><p>Rising Sea Levels</p></div></div></div><div class="w-12 h-0.5 bg-purple-600 mb-3"></div><div class="text-base text-gray-700 leading-relaxed" style="font-size: 16px; font-weight: 400; font-family: Poppins, sans-serif; color: rgb(55, 65, 81); line-height: 26px; text-align: start; margin: 0px; padding: 0px; border-radius: 0px; border: 0px solid rgb(229, 231, 235); background-color: rgba(0, 0, 0, 0); opacity: 1; box-shadow: none; text-shadow: none; text-decoration: none solid rgb(55, 65, 81); text-transform: none; letter-spacing: normal; word-spacing: 0px; text-overflow: clip; white-space: normal; word-break: normal; overflow: visible;"><div class="tiptap-text-editor w-full" style="line-height: inherit; font-size: inherit; font-weight: inherit; font-family: inherit; color: inherit; text-align: inherit;"><div contenteditable="true" data-placeholder="Enter text..." translate="no" class="tiptap ProseMirror outline-none focus:outline-none transition-all duration-200" tabindex="0"><p>Rising sea levels threaten coastal communities and ecosystems due to melting glaciers and thermal expansion.</p></div></div></div></div></div><div class="flex items-start space-x-4"><div class="flex-shrink-0 w-12 h-12 bg-white rounded-lg shadow-md flex items-center justify-center"><img src="/static/icons/bold/discord-logo-bold.png" alt="heatwave icon" class="w-6 h-6 object-contain text-gray-700" data-editable-processed="true" data-editable-id="2-icon-bulletPoints[1].icon-2" style="cursor: pointer; transition: opacity 0.2s, transform 0.2s;"></div><div class="flex-1"><div class="text-xl font-semibold text-gray-900 mb-2" style="font-size: 20px; font-weight: 600; font-family: Poppins, sans-serif; color: rgb(17, 24, 39); line-height: 28px; text-align: start; margin: 0px 0px 8px; padding: 0px; border-radius: 0px; border: 0px solid rgb(229, 231, 235); background-color: rgba(0, 0, 0, 0); opacity: 1; box-shadow: none; text-shadow: none; text-decoration: none solid rgb(17, 24, 39); text-transform: none; letter-spacing: normal; word-spacing: 0px; text-overflow: clip; white-space: normal; word-break: normal; overflow: visible;"><div class="tiptap-text-editor w-full" style="line-height: inherit; font-size: inherit; font-weight: inherit; font-family: inherit; color: inherit; text-align: inherit;"><div contenteditable="true" data-placeholder="Enter text..." translate="no" class="tiptap ProseMirror outline-none focus:outline-none transition-all duration-200" tabindex="0"><p>Intense Heatwaves</p></div></div></div><div class="w-12 h-0.5 bg-purple-600 mb-3"></div><div class="text-base text-gray-700 leading-relaxed" style="font-size: 16px; font-weight: 400; font-family: Poppins, sans-serif; color: rgb(55, 65, 81); line-height: 26px; text-align: start; margin: 0px; padding: 0px; border-radius: 0px; border: 0px solid rgb(229, 231, 235); background-color: rgba(0, 0, 0, 0); opacity: 1; box-shadow: none; text-shadow: none; text-decoration: none solid rgb(55, 65, 81); text-transform: none; letter-spacing: normal; word-spacing: 0px; text-overflow: clip; white-space: normal; word-break: normal; overflow: visible;"><div class="tiptap-text-editor w-full" style="line-height: inherit; font-size: inherit; font-weight: inherit; font-family: inherit; color: inherit; text-align: inherit;"><div contenteditable="true" data-placeholder="Enter text..." translate="no" class="tiptap ProseMirror outline-none focus:outline-none transition-all duration-200" tabindex="0"><p>Heatwaves are becoming more frequent and intense, posing significant risks to human health and agriculture.</p></div></div></div></div></div><div class="flex items-start space-x-4"><div class="flex-shrink-0 w-12 h-12 bg-white rounded-lg shadow-md flex items-center justify-center"><img src="/static/icons/bold/cloud-rain-bold.png" alt="precipitation changes icon" class="w-6 h-6 object-contain text-gray-700" data-editable-processed="true" data-editable-id="2-icon-bulletPoints[2].icon-3" style="cursor: pointer; transition: opacity 0.2s, transform 0.2s;"></div><div class="flex-1"><div class="text-xl font-semibold text-gray-900 mb-2" style="font-size: 20px; font-weight: 600; font-family: Poppins, sans-serif; color: rgb(17, 24, 39); line-height: 28px; text-align: start; margin: 0px 0px 8px; padding: 0px; border-radius: 0px; border: 0px solid rgb(229, 231, 235); background-color: rgba(0, 0, 0, 0); opacity: 1; box-shadow: none; text-shadow: none; text-decoration: none solid rgb(17, 24, 39); text-transform: none; letter-spacing: normal; word-spacing: 0px; text-overflow: clip; white-space: normal; word-break: normal; overflow: visible;"><div class="tiptap-text-editor w-full" style="line-height: inherit; font-size: inherit; font-weight: inherit; font-family: inherit; color: inherit; text-align: inherit;"><div contenteditable="true" data-placeholder="Enter text..." translate="no" class="tiptap ProseMirror outline-none focus:outline-none transition-all duration-200" tabindex="0"><p>Changes in Precipitation</p></div></div></div><div class="w-12 h-0.5 bg-purple-600 mb-3"></div><div class="text-base text-gray-700 leading-relaxed" style="font-size: 16px; font-weight: 400; font-family: Poppins, sans-serif; color: rgb(55, 65, 81); line-height: 26px; text-align: start; margin: 0px; padding: 0px; border-radius: 0px; border: 0px solid rgb(229, 231, 235); background-color: rgba(0, 0, 0, 0); opacity: 1; box-shadow: none; text-shadow: none; text-decoration: none solid rgb(55, 65, 81); text-transform: none; letter-spacing: normal; word-spacing: 0px; text-overflow: clip; white-space: normal; word-break: normal; overflow: visible;"><div class="tiptap-text-editor w-full" style="line-height: inherit; font-size: inherit; font-weight: inherit; font-family: inherit; color: inherit; text-align: inherit;"><div contenteditable="true" data-placeholder="Enter text..." translate="no" class="tiptap ProseMirror outline-none focus:outline-none transition-all duration-200" tabindex="0"><p>Altered precipitation patterns lead to increased droughts in some regions and severe flooding in others, affecting water resources.</p></div></div></div></div></div></div></div></div></div></div>
Output: 
const ImageSchema = z.object({
    __image_url__: z.url().meta({
        description: "URL to image",
    }),
    __image_prompt__: z.string().meta({
        description: "Prompt used to generate the image. Max 30 words",
    }).min(10).max(50),
})

const IconSchema = z.object({
    __icon_url__: z.string().meta({
        description: "URL to icon",
    }),
    __icon_query__: z.string().meta({
        description: "Query used to search the icon. Max 3 words",
    }).min(5).max(20),
})
const layoutId = "bullet-with-icons-slide"
const layoutName = "Bullet with Icons"
const layoutDescription = "A bullets style slide with main content, supporting image, and bullet points with icons and descriptions."

const Schema = z.object({
    title: z.string().min(3).max(40).default("Problem").meta({
        description: "Main title of the slide. Max 5 words",
    }),
    description: z.string().max(150).default("Businesses face challenges with outdated technology and rising costs, limiting efficiency and growth in competitive markets.").meta({
        description: "Main description text explaining the problem or topic. Max 30 words",
    }), 
    image: ImageSchema.default({
        __image_url__: 'https://images.unsplash.com/photo-1552664730-d307ca884978?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
        __image_prompt__: "Business people analyzing documents and charts in office"
    }).meta({
        description: "Supporting image for the slide. Max 30 words",
    }),
    bulletPoints: z.array(z.object({
        title: z.string().min(2).max(80).meta({
            description: "Bullet point title. Max 4 words",
        }),
        description: z.string().min(10).max(150).meta({
            description: "Bullet point description. Max 15 words",
        }),
        icon: IconSchema,
    })).min(1).max(3).default([
        {
            title: "Inefficiency",
            description: "Businesses struggle to find digital tools that meet their needs, causing operational slowdowns.",
            icon: {
                __icon_url__: "/static/icons/placeholder.png",
                __icon_query__: "warning alert inefficiency"
            }
        },
        {
            title: "High Costs",
            description: "Outdated systems increase expenses, while small businesses struggle to expand their market reach.",
            icon: {
                __icon_url__: "/static/icons/placeholder.png",
                __icon_query__: "trending up costs chart"
            }
        }
    ]).meta({
        description: "List of bullet points with icons and descriptions. Max 3 points",
    })
})

type BulletWithIconsSlideData = z.infer<typeof Schema>

interface BulletWithIconsSlideLayoutProps {
    data?: Partial<BulletWithIconsSlideData>
}

const dynamicSlideLayout: React.FC<BulletWithIconsSlideLayoutProps> = ({ data: slideData }) => {
    const bulletPoints = slideData?.bulletPoints || []

    return (
        <>
            <div 
                className="w-full rounded-sm max-w-[1280px] shadow-lg max-h-[720px] aspect-video bg-gradient-to-br from-gray-50 to-white relative z-20 mx-auto overflow-hidden"
                style={{
                    fontFamily: "Poppins, sans-serif"
                }}
            >


                {/* Main Content */}
                <div className="flex flex-col h-full px-8 sm:px-12 lg:px-20 pt-8 pb-8">
                    {/* Title Section - Full Width */}
                    <div className="mb-8">
                        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900">
                            {slideData?.title || "Problem"}
                        </h1>
                    </div>

                    {/* Content Container */}
                    <div className="flex flex-1">
                        {/* Left Section - Image with Grid Pattern */}
                        <div className="flex-1 relative">
                        {/* Grid Pattern Background */}
                        <div className="absolute top-0 left-0 w-full h-full">
                            <svg className="w-full h-full opacity-30" viewBox="0 0 200 200">
                                <defs>
                                    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                                        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#8b5cf6" strokeWidth="0.5"/>
                                    </pattern>
                                </defs>
                                <rect width="100%" height="100%" fill="url(#grid)" />
                            </svg>
                        </div>
                        
                        {/* Image Container */}
                        <div className="relative z-10 h-full flex items-center justify-center p-4">
                            <div className="w-full max-w-md h-80 rounded-2xl overflow-hidden shadow-lg">
                                <img
                                    src={slideData?.image?.__image_url__ || ""}
                                    alt={slideData?.image?.__image_prompt__ || slideData?.title || ""}
                                    className="w-full h-full object-cover"
                                />
                            </div>
                        </div>

                        {/* Decorative Sparkle */}
                        <div className="absolute top-20 right-8 text-purple-600">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 0l3.09 6.26L22 9l-6.91 2.74L12 18l-3.09-6.26L2 9l6.91-2.74L12 0z"/>
                            </svg>
                        </div>
                    </div>

                        {/* Right Section - Content */}
                        <div className="flex-1 flex flex-col justify-center pl-8 lg:pl-16">
                            {/* Description */}
                            <p className="text-lg text-gray-700 leading-relaxed mb-8">
                                {slideData?.description || "Businesses face challenges with outdated technology and rising costs, limiting efficiency and growth in competitive markets."}
                            </p>

                        {/* Bullet Points */}
                        <div className="space-y-6">
                            {bulletPoints.map((bullet, index) => (
                                <div key={index} className="flex items-start space-x-4">
                                    {/* Icon */}
                                    <div className="flex-shrink-0 w-12 h-12 bg-white rounded-lg shadow-md flex items-center justify-center">
                                        <img 
                                            src={bullet.icon.__icon_url__} 
                                            alt={bullet.icon.__icon_query__}
                                            className="w-6 h-6 object-contain text-gray-700"
                                        />
                                    </div>
                                    
                                    {/* Content */}
                                    <div className="flex-1">
                                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                            {bullet.title}
                                        </h3>   
                                        <div className="w-12 h-0.5 bg-purple-600 mb-3"></div>
                                        <p className="text-base text-gray-700 leading-relaxed">
                                            {bullet.description}
                                        </p>
                                    </div>
                                </div>
                            ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

- Give output with only code and nothing else. (no json, no markdown, no text, no explanation)
"""

HTML_EDIT_SYSTEM_PROMPT = """
你需要根据UI中的指示和草图来编辑给定的html。你将获得当前UI的代码（演示文稿大小），以及其图像形式的可视化。此外，你还会得到另一张图像，其中包含UI中可能发生变化的草图指示。你需要返回编辑后的html和tailwind，应用图像和提示中指示的更改。确保在做出更改之前仔细考虑设计，同时确保不要更改未指示的部分。尝试为生成的内容遵循当前内容的设计风格。如果未提供草图图像，则需要根据提示编辑html。确保演示文稿的大小在任何情况下都不会改变。只输出代码，不添加其他内容。
"""

