import {assertType, describe , it , expectTypeOf} from "vitest";
import {Winder} from "../types";


describe("Global Test", (): void => {
    it("Global Function Test" , (): void => {
        assertType<Winder>(winder)
        expectTypeOf(winder.getQuery).parameter(0).toEqualTypeOf<string | undefined>()
    })

    it("Global properties Test", (): void => {
        assertType<string>(fetchContent(''))
    })
})
