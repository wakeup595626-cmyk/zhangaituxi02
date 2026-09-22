// Copyright Epic Games, Inc. All Rights Reserved.


#include "zhangaituxi02PlayerController.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/LocalPlayer.h"
#include "InputMappingContext.h"
#include "Blueprint/UserWidget.h"
#include "Components/InputComponent.h"
#include "EngineUtils.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerStart.h"
#include "InputCoreTypes.h"
#include "Kismet/KismetSystemLibrary.h"
#include "zhangaituxi02.h"
#include "Widgets/Input/SVirtualJoystick.h"

void Azhangaituxi02PlayerController::BeginPlay()
{
	Super::BeginPlay();

	// only spawn touch controls on local player controllers
	if (SVirtualJoystick::ShouldDisplayTouchInterface() && IsLocalPlayerController())
	{
		// spawn the mobile controls widget
		MobileControlsWidget = CreateWidget<UUserWidget>(this, MobileControlsWidgetClass);

		if (MobileControlsWidget)
		{
			// add the controls to the player screen
			MobileControlsWidget->AddToPlayerScreen(0);

		} else {

			UE_LOG(Logzhangaituxi02, Error, TEXT("Could not spawn mobile controls widget."));

		}

	}
}

void Azhangaituxi02PlayerController::OnPossess(APawn* InPawn)
{
	Super::OnPossess(InPawn);

	if (InPawn == nullptr)
	{
		return;
	}

	if (UWorld* World = GetWorld())
	{
		for (TActorIterator<APlayerStart> PlayerStart(World); PlayerStart; ++PlayerStart)
		{
			if (PlayerStart->GetClass() != APlayerStart::StaticClass())
			{
				continue;
			}

			InPawn->SetActorLocationAndRotation(
				PlayerStart->GetActorLocation(),
				PlayerStart->GetActorRotation(),
				false,
				nullptr,
				ETeleportType::TeleportPhysics);
			break;
		}
	}
}

void Azhangaituxi02PlayerController::SetupInputComponent()
{
	Super::SetupInputComponent();

	if (InputComponent)
	{
		InputComponent->BindKey(EKeys::Escape, IE_Pressed, this, &Azhangaituxi02PlayerController::HandleQuitPressed);
	}

	// only add IMCs for local player controllers
	if (IsLocalPlayerController())
	{
		// Add Input Mapping Contexts
		if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(GetLocalPlayer()))
		{
			for (UInputMappingContext* CurrentContext : DefaultMappingContexts)
			{
				Subsystem->AddMappingContext(CurrentContext, 0);
			}

			// only add these IMCs if we're not using mobile touch input
			if (!SVirtualJoystick::ShouldDisplayTouchInterface())
			{
				for (UInputMappingContext* CurrentContext : MobileExcludedMappingContexts)
				{
					Subsystem->AddMappingContext(CurrentContext, 0);
				}
			}
		}
	}
}

void Azhangaituxi02PlayerController::HandleQuitPressed()
{
	UKismetSystemLibrary::QuitGame(this, this, EQuitPreference::Quit, false);
}
