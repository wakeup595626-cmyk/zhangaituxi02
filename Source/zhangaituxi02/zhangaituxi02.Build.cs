// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class zhangaituxi02 : ModuleRules
{
	public zhangaituxi02(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"zhangaituxi02",
			"zhangaituxi02/Variant_Platforming",
			"zhangaituxi02/Variant_Platforming/Animation",
			"zhangaituxi02/Variant_Combat",
			"zhangaituxi02/Variant_Combat/AI",
			"zhangaituxi02/Variant_Combat/Animation",
			"zhangaituxi02/Variant_Combat/Gameplay",
			"zhangaituxi02/Variant_Combat/Interfaces",
			"zhangaituxi02/Variant_Combat/UI",
			"zhangaituxi02/Variant_SideScrolling",
			"zhangaituxi02/Variant_SideScrolling/AI",
			"zhangaituxi02/Variant_SideScrolling/Gameplay",
			"zhangaituxi02/Variant_SideScrolling/Interfaces",
			"zhangaituxi02/Variant_SideScrolling/UI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
