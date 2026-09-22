// Copyright Epic Games, Inc. All Rights Reserved.

#include "NPCMusicTriggerPad.h"

#include "Components/AudioComponent.h"
#include "Components/BoxComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/Pawn.h"
#include "Sound/SoundBase.h"
#include "UObject/ConstructorHelpers.h"

ANPCMusicTriggerPad::ANPCMusicTriggerPad()
{
	PrimaryActorTick.bCanEverTick = false;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	SetRootComponent(SceneRoot);

	TriggerVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("TriggerVolume"));
	TriggerVolume->SetupAttachment(SceneRoot);
	TriggerVolume->SetRelativeLocation(FVector(0.0f, 0.0f, 75.0f));
	TriggerVolume->SetBoxExtent(FVector(95.0f, 95.0f, 85.0f));
	TriggerVolume->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	TriggerVolume->SetCollisionObjectType(ECC_WorldDynamic);
	TriggerVolume->SetCollisionResponseToAllChannels(ECR_Ignore);
	TriggerVolume->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	TriggerVolume->SetGenerateOverlapEvents(true);

	PadMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PadMesh"));
	PadMesh->SetupAttachment(SceneRoot);
	PadMesh->SetRelativeLocation(FVector(0.0f, 0.0f, 6.0f));
	PadMesh->SetRelativeScale3D(FVector(1.25f, 1.25f, 0.12f));
	PadMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	PadMesh->SetCastShadow(false);
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMesh(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	if (CylinderMesh.Succeeded())
	{
		PadMesh->SetStaticMesh(CylinderMesh.Object);
	}

	PadLabel = CreateDefaultSubobject<UTextRenderComponent>(TEXT("PadLabel"));
	PadLabel->SetupAttachment(SceneRoot);
	PadLabel->SetRelativeLocation(FVector(-4.0f, 0.0f, 85.0f));
	PadLabel->SetRelativeRotation(FRotator(0.0f, 180.0f, 0.0f));
	PadLabel->SetHorizontalAlignment(EHorizTextAligment::EHTA_Center);
	PadLabel->SetVerticalAlignment(EVerticalTextAligment::EVRTA_TextCenter);
	PadLabel->SetWorldSize(30.0f);
	PadLabel->SetTextRenderColor(FColor(255, 218, 88));
	PadLabel->SetText(FText::FromString(TEXT("BGM")));
	PadLabel->SetCastShadow(false);

	PadLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("PadLight"));
	PadLight->SetupAttachment(SceneRoot);
	PadLight->SetRelativeLocation(FVector(0.0f, 0.0f, 30.0f));
	PadLight->SetIntensity(500.0f);
	PadLight->SetAttenuationRadius(260.0f);
	PadLight->SetCastShadows(false);
	PadLight->SetLightColor(AccentColor);

	AudioComponent = CreateDefaultSubobject<UAudioComponent>(TEXT("AudioComponent"));
	AudioComponent->SetupAttachment(SceneRoot);
	AudioComponent->bAutoActivate = false;
	AudioComponent->bIsUISound = true;
	AudioComponent->bOverrideAttenuation = true;
	AudioComponent->AttenuationOverrides.bAttenuate = false;

	ButtonLabel = FText::FromString(TEXT("BGM"));
}

void ANPCMusicTriggerPad::OnConstruction(const FTransform& Transform)
{
	Super::OnConstruction(Transform);

	if (PadLabel)
	{
		PadLabel->SetText(ButtonLabel);
		PadLabel->SetTextRenderColor(AccentColor.ToFColor(true));
	}

	if (PadLight)
	{
		PadLight->SetLightColor(AccentColor);
	}
}

void ANPCMusicTriggerPad::BeginPlay()
{
	Super::BeginPlay();

	TriggerVolume->OnComponentBeginOverlap.AddDynamic(this, &ANPCMusicTriggerPad::HandleTriggerBeginOverlap);
	TriggerVolume->OnComponentEndOverlap.AddDynamic(this, &ANPCMusicTriggerPad::HandleTriggerEndOverlap);
	AudioComponent->OnAudioFinished.AddDynamic(this, &ANPCMusicTriggerPad::HandleMusicFinished);
}

void ANPCMusicTriggerPad::HandleTriggerBeginOverlap(
	UPrimitiveComponent* OverlappedComponent,
	AActor* OtherActor,
	UPrimitiveComponent* OtherComponent,
	int32 OtherBodyIndex,
	bool bFromSweep,
	const FHitResult& SweepResult)
{
	if (APawn* PlayerPawn = Cast<APawn>(OtherActor); PlayerPawn && PlayerPawn->IsPlayerControlled())
	{
		PlayerPawnsInside.Add(PlayerPawn);
		StartMusic();
	}
}

void ANPCMusicTriggerPad::HandleTriggerEndOverlap(
	UPrimitiveComponent* OverlappedComponent,
	AActor* OtherActor,
	UPrimitiveComponent* OtherComponent,
	int32 OtherBodyIndex)
{
	if (APawn* PlayerPawn = Cast<APawn>(OtherActor); PlayerPawn && PlayerPawn->IsPlayerControlled())
	{
		PlayerPawnsInside.Remove(PlayerPawn);
		if (PlayerPawnsInside.IsEmpty())
		{
			StopMusic();
		}
	}
}

void ANPCMusicTriggerPad::HandleMusicFinished()
{
	if (bLoopMusic && !PlayerPawnsInside.IsEmpty() && Music)
	{
		AudioComponent->Play();
	}
}

void ANPCMusicTriggerPad::StartMusic()
{
	if (!Music)
	{
		return;
	}

	if (AudioComponent->GetSound() != Music)
	{
		AudioComponent->SetSound(Music);
	}

	if (!AudioComponent->IsPlaying())
	{
		UE_LOG(LogTemp, Display, TEXT("NPCMusicTriggerPad '%s' is playing '%s'"), *GetName(), *GetNameSafe(Music));
		AudioComponent->FadeIn(FadeInSeconds, 1.0f, 0.0f);
	}
}

void ANPCMusicTriggerPad::StopMusic()
{
	if (AudioComponent->IsPlaying())
	{
		UE_LOG(LogTemp, Display, TEXT("NPCMusicTriggerPad '%s' is fading out"), *GetName());
		AudioComponent->FadeOut(FadeOutSeconds, 0.0f);
	}
}

bool ANPCMusicTriggerPad::IsPlayerPawn(const AActor* Actor) const
{
	const APawn* Pawn = Cast<APawn>(Actor);
	return Pawn && Pawn->IsPlayerControlled();
}
