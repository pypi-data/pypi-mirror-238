<template>
  <div id="mission-amend-timing" :class="$style['mission-amend-timing']">
    <div class="p-2">
      <USelectWrapper
        label="label"
        label-text="Mission Leg To Amend"
        placeholder="Please select Flight Leg"
        :options="activeLegs"
        :loading="isFetchingMission"
        :clearable="false"
        :append-to-body="false"
        required
        v-model="state.leg"
        :errors="v$.leg.$errors"
        :is-validation-dirty="v$.leg.$dirty"
      />
      <USelectWrapper
        label="label"
        label-text="Movement To Amend"
        placeholder="Please select Movement"
        :options="movements"
        :loading="isFetchingMission"
        :clearable="false"
        :append-to-body="false"
        required
        :disabled="!state.leg"
        v-model="state.movement"
        :errors="v$.movement.$errors"
        :is-validation-dirty="v$.movement.$dirty"
      />
      <ULabel required label-text="New Movement Date & Time" />
      <UFlatPickr
        ref="departureDateRef"
        placeholder="Select date"
        :config="{
          allowInput: true,
          altInput: true,
          altFormat: 'Y-m-d H:i',
          dateFormat: 'Y-m-d H:i',
          enableTime: true,
          time_24hr: true,
          minuteIncrement: 1
        }"
        class="mb-[1rem]"
        required
        :disabled="!state.movement"
        v-model="state.newDatetime"
        :errors="v$.newDatetime.$errors"
        :is-validation-dirty="v$.newDatetime.$dirty"
      />
      <UTimeDurationPickr
        :label="changedByLabel"
        requied
        v-model="state.changedBy"
        :disabled="!state.movement"
        :errors="v$.changedBy.$errors"
        :is-validation-dirty="v$.changedBy.$dirty"
      />
      <UCheckboxWrapper
        label="change_all_subsequent"
        label-text="Roll Change to All Subsequent Mission Legs?"
        v-model="state.roll_change_to_subsequent_legs"
        :class="$style['flex-reverse']"
      />
    </div>
    <div class="border-b border-b-[#e5e7eb] mt-[25px]"></div>
    <div :class="$style['mission-amend-timing__actions']">
      <div class="flex items-center gap-x-2">
        <button
          data-bs-dismiss="modal"
          type="button"
          class="!bg-gray-200 !text-grey-900"
          :class="[$style['mission-amend-timing__service-btn']]"
        >
          Close
        </button>
        <button
          :class="[
            $style['mission-amend-timing__service-btn'],
            $style['mission-amend-timing__service-btn--submit']
          ]"
          class="!bg-green-700 !text-black-400"
          @click="onSubmit"
        >
          Update Timings
        </button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, reactive, ref, watchEffect } from 'vue'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import USelectWrapper from '@/components/ui/wrappers/USelectWrapper.vue'
import ULabel from '@/components/ui/form/ULabel.vue'
import UFlatPickr from '@/components/ui/form/UFlatPickr/UFlatPickr.vue'
import UCheckboxWrapper from '@/components/ui/wrappers/UCheckboxWrapper.vue'
import UTimeDurationPickr from '@/components/ui/form/UTimeDurationPickr.vue'
import { useVuelidate } from '@vuelidate/core'
import { required } from '@vuelidate/validators'
import { useFetch } from '@/composables/useFetch'
import Mission from '@/services/mission/mission'
import { notify } from '@/helpers/toast'
import type {
  IAmendTiming,
  IExtendedMission,
  IExtendedMissionLeg,
} from '@/types/mission/mission.types'
import { getMissionId, redirectToURL } from '@/helpers'

dayjs.extend(utc)

const {
  data: mission,
  loading: isFetchingMission,
  callFetch: fetchMission
} = useFetch<IExtendedMission, (missionId: number) => Promise<IExtendedMission>>(
  async (missionId: number) => {
    const { data } = await Mission.getMission(missionId)

    return data
  }
)

const activeLegs = computed(() => {
  if (!mission.value) {
    return []
  }

  return mission.value.legs?.map((leg: IExtendedMissionLeg) => ({
    label: `Flight Leg ${leg.sequence_id} - ${leg.departure_location.tiny_repr}>${leg.arrival_location.tiny_repr}`,
    value: leg.id
  }))
})

const movements = computed(() => {
  if (!state.leg?.value) {
    return []
  }

  const selectedLeg = mission.value?.legs.find(
    (leg: IExtendedMissionLeg) => leg.id === state.leg.value
  )

  if (!selectedLeg) {
    return []
  }

  return [
    {
      //   label: `Departure - ${selectedLeg.departure_datetime}`,
      label: `Departure - ${dayjs.utc(selectedLeg.departure_datetime).format('MMM-DD-YYYY HH:mm')}`,
      datetime: selectedLeg.departure_datetime,
      value: 'departure'
    },
    {
      //   label: `Arrival - ${selectedLeg.arrival_datetime}`,
      label: `Arrival - ${dayjs.utc(selectedLeg.arrival_datetime).format('MMM-DD-YYYY HH:mm')}`,
      datetime: selectedLeg.arrival_datetime,
      value: 'arrival'
    }
  ]
})

const state = reactive<any>({
  leg: null,
  movement: null,
  newDatetime: null,
  changedBy: null
})

const rules = computed(() => ({
  leg: {
    required
  },
  movement: {
    required
  },
  newDatetime: {
    required
  },
  changedBy: {
    required
  }
}))

const changedByLabel = computed(() => {
  return state.changedBy === undefined
    ? 'Movement changed By'
    : state.changedBy > 0
    ? 'Movement Delayed By'
    : 'Movement Brought Forward by'
})

watchEffect(() => {
  if (!state.newDatetime || !state.movement) {
    return
  }

  state.changedBy = dayjs.utc(state.newDatetime).diff(dayjs.utc(state.movement.datetime))
})

watchEffect(() => {
  if (!state.changedBy || !state.movement) {
    return
  }

  state.newDatetime = dayjs
    .utc(state.movement.datetime)
    .add(state.changedBy)
    .format('YYYY-MM-DD HH:mm')
})

const v$ = useVuelidate(rules, state)

const onSubmit = async () => {
  try {
    const isValid = await v$?.value?.$validate()
    if (!isValid) {
      return notify('Error while submitting, form is not valid!', 'error')
    } else {
      if (state.leg.value) {
        const amend_timinng: IAmendTiming = {
          movement_direction: state.movement.value,
          new_datetime: state.newDatetime,
          roll_change_to_subsequent_legs: state.roll_change_to_subsequent_legs
        }
        await Mission.putMissionAmendTiming(state.leg.value, amend_timinng)
        redirectToURL(getMissionId() as number)
        notify('Amend mission timings successfully!', 'success')
      }
    }
  } catch (error) {
    return notify('Error while submitting, server error', 'error')
  }
}

const fetchData = () => {
  const missionId = getMissionId() as number
  fetchMission(missionId)
}

onMounted(fetchData)
</script>
<style scoped lang="scss"></style>

<style module lang="scss">
.mission-amend-timing {
  @apply relative flex flex-col bg-white min-w-0 rounded-[0.5rem] pb-2;

  .flex-reverse {
    flex-direction: row-reverse;
    justify-content: flex-end;
    align-items: flex-start;
    margin-top: 2px;
    column-gap: 8px;
  }

  &__actions {
    @apply flex items-center justify-end mt-2 px-2;
  }

  &__service-btn {
    @apply text-sm flex shrink-0 focus:shadow-none rounded-md text-white mb-0 mt-2 p-2 px-4 w-fit #{!important};

    &--primary {
      @apply bg-grey-900 #{!important};
    }

    &--submit {
      @apply bg-confetti-500 text-gray-900 #{!important};
    }
  }
}
</style>
