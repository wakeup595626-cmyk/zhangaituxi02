// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class zhangaituxi02EditorTarget : TargetRules
{
	public zhangaituxi02EditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		WindowsPlatform.Compiler = WindowsCompiler.VisualStudio2026;
		DefaultBuildSettings = BuildSettingsVersion.V7;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;
		ExtraModuleNames.Add("zhangaituxi02");
	}
}
