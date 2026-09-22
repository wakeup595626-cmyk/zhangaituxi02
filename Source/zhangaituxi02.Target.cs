// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class zhangaituxi02Target : TargetRules
{
	public zhangaituxi02Target(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		WindowsPlatform.Compiler = WindowsCompiler.VisualStudio2026;
		DefaultBuildSettings = BuildSettingsVersion.V7;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;
		ExtraModuleNames.Add("zhangaituxi02");
	}
}
