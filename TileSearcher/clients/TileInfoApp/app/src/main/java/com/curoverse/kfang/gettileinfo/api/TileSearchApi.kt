package com.curoverse.kfang.gettileinfo.api

import com.curoverse.kfang.gettileinfo.model.TileInfo
import io.reactivex.Observable
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query

/**
 * Tile search API with Retrofit
 */
interface TileSearchApi {
    @GET("/tile?json=true&all=true")
    fun getTile(@Query("index") index: Int) : Observable<TileInfo>
}