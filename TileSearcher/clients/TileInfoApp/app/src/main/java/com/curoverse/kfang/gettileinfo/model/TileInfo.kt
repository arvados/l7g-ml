package com.curoverse.kfang.gettileinfo.model

import android.os.Parcel
import android.os.Parcelable

/**
 * TileInfo data class
 */
data class TileInfo (val search: ArrayList<String>,
                       val base_pair_start: String,
                       val base_pair_end: String,
                       val tile_path: String,
                       val tile_step: String,
                       val tile_phase: String,
                       val name: String,
                       val variants: ArrayList<String>) : Parcelable {
    companion object {
        @Suppress("unused")
        @JvmField val CREATOR: Parcelable.Creator<TileInfo> = object : Parcelable.Creator<TileInfo> {
            override fun createFromParcel(source: Parcel): TileInfo = TileInfo(source)
            override fun newArray(size: Int): Array<TileInfo?> = arrayOfNulls(size)
        }
    }

    constructor(source: Parcel) : this(
        source.createStringArrayList(),
        source.readString(),
        source.readString(),
        source.readString(),
        source.readString(),
        source.readString(),
        source.readString(),
        source.createStringArrayList()
    )

    override fun describeContents() = 0

    override fun writeToParcel(dest: Parcel, flags: Int) {
        dest.writeStringList(search)
        dest.writeString(base_pair_start)
        dest.writeString(base_pair_end)
        dest.writeString(tile_path)
        dest.writeString(tile_step)
        dest.writeString(tile_phase)
        dest.writeString(name)
        dest.writeStringList(variants)
    }
}
