// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "NPCMusicTriggerPad.generated.h"

class UAudioComponent;
class UBoxComponent;
class UPointLightComponent;
class USceneComponent;
class USoundBase;
class UStaticMeshComponent;
class UTextRenderComponent;

/**
 * Reusable floor button that plays one NPC's music while the player stands on it.
 * Configure a different Music asset and ButtonLabel on each placed instance.
 */
UCLASS(Blueprintable)
class ZHANGAITUXI02_API ANPCMusicTriggerPad : public AActor
{
	GENERATED_BODY()

public:
	ANPCMusicTriggerPad();

	virtual void OnConstruction(const FTransform& Transform) override;

protected:
	virtual void BeginPlay() override;

	UFUNCTION()
	void HandleTriggerBeginOverlap(
		UPrimitiveComponent* OverlappedComponent,
		AActor* OtherActor,
		UPrimitiveComponent* OtherComponent,
		int32 OtherBodyIndex,
		bool bFromSweep,
		const FHitResult& SweepResult);

	UFUNCTION()
	void HandleTriggerEndOverlap(
		UPrimitiveComponent* OverlappedComponent,
		AActor* OtherActor,
		UPrimitiveComponent* OtherComponent,
		int32 OtherBodyIndex);

	UFUNCTION()
	void HandleMusicFinished();

	void StartMusic();
	void StopMusic();
	bool IsPlayerPawn(const AActor* Actor) const;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	TObjectPtr<USceneComponent> SceneRoot;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	TObjectPtr<UBoxComponent> TriggerVolume;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	TObjectPtr<UStaticMeshComponent> PadMesh;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	TObjectPtr<UTextRenderComponent> PadLabel;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	TObjectPtr<UPointLightComponent> PadLight;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
	TObjectPtr<UAudioComponent> AudioComponent;

	/** Sound played only while at least one player is standing on the pad. */
	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category = "Music")
	TObjectPtr<USoundBase> Music;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Music", meta = (ClampMin = "0.0"))
	float FadeInSeconds = 0.25f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Music", meta = (ClampMin = "0.0"))
	float FadeOutSeconds = 0.50f;

	/** Replays the track if it finishes while the player is still on the pad. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Music")
	bool bLoopMusic = true;

	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category = "Presentation")
	FText ButtonLabel;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Presentation")
	FLinearColor AccentColor = FLinearColor(1.0f, 0.10f, 0.22f, 1.0f);

private:
	TSet<TWeakObjectPtr<APawn>> PlayerPawnsInside;
};
